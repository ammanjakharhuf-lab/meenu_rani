// Planar (depth-averaged) tumour-immune-angiogenesis model of melanoma with
// surgical excision and anti-VEGF antibody therapy.
//
// Build:  g++ -O3 -march=native -fopenmp -o melanoma_vegf melanoma_vegf.cpp
// Usage:  melanoma_vegf <param-file> [key=value ...]
//
// All state variables are dimensionless densities on a uniform 2-D Cartesian
// grid; space is in mm and time in days. See manuscript Table 2 for meanings.

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <map>
#include <random>
#include <sstream>
#include <string>
#include <vector>

struct Params {
  std::map<std::string, double> v;
  std::map<std::string, std::string> s;
  double operator[](const std::string& k) const {
    auto it = v.find(k);
    if (it == v.end()) { fprintf(stderr, "missing parameter %s\n", k.c_str()); exit(1); }
    return it->second;
  }
  void set(const std::string& line) {
    auto p = line.find('=');
    if (p == std::string::npos) return;
    std::string k = line.substr(0, p), val = line.substr(p + 1);
    auto trim = [](std::string& x) {
      size_t a = x.find_first_not_of(" \t"), b = x.find_last_not_of(" \t\r");
      x = (a == std::string::npos) ? "" : x.substr(a, b - a + 1);
    };
    trim(k); trim(val);
    if (k.empty() || k[0] == '#') return;
    char* end = nullptr;
    double d = strtod(val.c_str(), &end);
    if (end && *end == '\0' && !val.empty()) v[k] = d; else s[k] = val;
  }
};

int main(int argc, char** argv) {
  if (argc < 2) { fprintf(stderr, "usage: %s params.txt [k=v ...]\n", argv[0]); return 1; }
  Params P;
  { std::ifstream f(argv[1]); std::string line;
    while (std::getline(f, line)) { auto h = line.find('#'); if (h != std::string::npos) line = line.substr(0, h); P.set(line); } }
  for (int i = 2; i < argc; ++i) P.set(argv[i]);

  const std::string out = P.s.count("out") ? P.s["out"] : "run";
  // ---- grid ----
  const double L = P["L"], dx = P["dx"], dt = P["dt"], tend = P["t_end"];
  const int N = (int)std::lround(L / dx) + 1, NN = N * N;
  const double xc = 0.5 * L, yc = 0.5 * L;
  // ---- parameters ----
  const double Dc = P["D_c"], ac = P["alpha_c"], dc = P["delta_c"], th1 = P["theta_1"], th2 = P["theta_2"];
  const double lsig = P["lambda_sigma"], kn = P["kappa_n"];
  const double tau0 = P["tau_0"], tauA = P["tau_A"], lamc = P["lambda_c"], xi = P["xi"];
  const double Dm = P["D_m"], chi = P["chi_m"], qm = P["q_m"], phia = P["phi_a"], omega = P["omega"];
  const double vI = P["v_I"], bK = P["beta_K"], bm = P["beta_m"];
  const double Da = P["D_a"], gac = P["gamma_ac"], gam = P["gamma_am"], ba = P["beta_a"];
  const double Dv = P["D_v"], gv = P["gamma_v"], av = P["alpha_v"], gvm = P["gamma_vm"], bv = P["beta_v"],
               bX = P["beta_X"], muv = P["mu_v"], KD = P["K_D"];
  const double Db = P["D_b"], ab = P["alpha_b"], bmax = P["b_max"], db = P["delta_b"];
  const double DA = P["D_A"], PA = P["P_A"], bA = P["beta_A"];
  const double kP = P["k_P"], MP = P["M_P"], bP = P["beta_P"];
  const double Kcell = P["K_cells"], H = P["H"];
  const double cellsPerNode = Kcell * H * dx * dx;
  // treatment
  const double t_s = P["t_surgery"], margin = P["margin"];
  const double thalf = P["t_half"], kel = std::log(2.0) / thalf, C0 = P["C0"] * P["dose_frac"];
  const double d_start = P["drug_start"], d_stop = P["drug_stop"], d_int = P["drug_interval"];
  const double io_start = P["io_start"], io_stop = P["io_stop"], io_eff = P["io_eff"], io_gain = P["io_gain"];
  // seeding
  const double lam0 = P["lambda_seed"], Mref = P["M_ref"], lamd = P["lambda_dist"], s0 = P["s0"], ws = P["w_seed"];
  const double c_init = P["c_init"], r_init = P["r_init"];
  const double Mdet = P["M_det"];
  std::mt19937_64 rng((unsigned long long)P["seed"]);
  std::uniform_real_distribution<double> U(0.0, 1.0);

  std::vector<double> c(NN, 0), s(NN, 0), V(NN, 0), b(NN, 1), m(NN, 0), a(NN, 0), A(NN, 0);
  std::vector<double> c2(NN), s2(NN), V2(NN), b2(NN), m2(NN), a2(NN), A2(NN);
  std::vector<double> Tn(NN), sig(NN), vfree(NN), Gam(NN);
  for (int j = 0; j < N; ++j)
    for (int i = 0; i < N; ++i) {
      double r2 = (i * dx - xc) * (i * dx - xc) + (j * dx - yc) * (j * dx - yc);
      c[j * N + i] = c_init * std::exp(-r2 / (2 * r_init * r_init));
    }

  // snapshot times
  std::vector<double> snaps;
  if (P.s.count("snapshots")) { std::stringstream ss(P.s["snapshots"]); std::string tok;
    while (std::getline(ss, tok, ',')) snaps.push_back(atof(tok.c_str())); }
  else if (P.v.count("snapshots")) snaps.push_back(P["snapshots"]);
  size_t snapIdx = 0;

  FILE* ts = fopen((out + "_ts.csv").c_str(), "w");
  fprintf(ts, "t,M_c,M_s,M_m,neovasc,vfree_max,vfree_tumor,Cp,A_mean,P,r_p,n_sat,recruit\n");
  FILE* ev = fopen((out + "_events.csv").c_str(), "w");
  fprintf(ev, "t,type,x,y,dist_from_edge\n");

  double Ppr = 0.0, Cp = 0.0;
  bool operated = false; int nsat = 0;
  double nextDose = d_start;
  double t_rec = -1;
  const long nsteps = (long)std::lround(tend / dt);
  const int outEvery = (int)std::lround(1.0 / dt);
  auto idx = [N](int i, int j) { i = i < 0 ? 1 : (i >= N ? N - 2 : i); j = j < 0 ? 1 : (j >= N ? N - 2 : j); return j * N + i; };
  const double inv = 1.0 / (dx * dx);

  for (long step = 0; step <= nsteps; ++step) {
    double t = step * dt;
    // ---- pharmacokinetics (one-compartment, bolus dosing) ----
    if (C0 > 0 && t + 1e-9 >= nextDose && nextDose < d_stop - 1e-9) { Cp += C0; nextDose += d_int; }
    // ---- diagnostics ----
    double Mc = 0, Ms = 0, Mm = 0, neo = 0, vmax = 0, vt = 0, Tsum = 0, Am = 0, rec = 0; int ntum = 0;
    for (int k = 0; k < NN; ++k) {
      Mc += c[k]; Ms += s[k]; Mm += m[k]; neo += (b[k] - 1.0); Am += A[k];
      double T = c[k] + s[k];
      double vf = V[k] * KD / (KD + A[k]);
      if (vf > vmax) vmax = vf;
      vt += vf * T; Tsum += T;
      if (c[k] > 0.05) ntum++;
    }
    Mc *= cellsPerNode; Ms *= cellsPerNode; Mm *= cellsPerNode; neo *= dx * dx; Am /= NN;
    double rp = std::sqrt(ntum * dx * dx / M_PI);
    // ---- surgery ----
    if (!operated && t + 1e-9 >= t_s) {
      operated = true;
      double re = rp + margin;
      for (int j = 0; j < N; ++j) for (int i = 0; i < N; ++i) {
        double r = std::hypot(i * dx - xc, j * dx - yc);
        if (r <= re) { int k = j * N + i; c[k] = 0; s[k] = 0; V[k] = 0; b[k] = 1; m[k] = 0; a[k] = 0; }
      }
      fprintf(ev, "%.3f,surgery,%.3f,%.3f,%.3f\n", t, xc, yc, re);
    }
    // ---- metastatic seeding (Poisson, rate proportional to primary burden) ----
    if (!operated && lam0 > 0) {
      double lam = lam0 * Mc / Mref;
      if (U(rng) < lam * dt) {
        double ang = 2 * M_PI * U(rng);
        double dist = -std::log(1.0 - U(rng)) / lamd;
        double r = rp + dist;
        double x = xc + r * std::cos(ang), y = yc + r * std::sin(ang);
        if (x > 1 && x < L - 1 && y > 1 && y < L - 1) {
          nsat++;
          for (int j = 0; j < N; ++j) for (int i = 0; i < N; ++i) {
            double d2 = (i * dx - x) * (i * dx - x) + (j * dx - y) * (j * dx - y);
            if (d2 < 9 * ws * ws) s[j * N + i] += s0 * std::exp(-d2 / (2 * ws * ws));
          }
          fprintf(ev, "%.3f,seed,%.3f,%.3f,%.3f\n", t, x, y, dist);
        }
      }
    }
    // ---- algebraic closures ----
    for (int k = 0; k < NN; ++k) {
      double T = c[k] + s[k]; Tn[k] = T;
      { double sup = kn + b[k] - 1.0; sig[k] = sup / (sup + lsig * T); }
      vfree[k] = V[k] * KD / (KD + A[k]);
      Gam[k] = T / (xi + T);
    }
    if (step % outEvery == 0) {
      double rsum = 0;
      for (int k = 0; k < NN; ++k) rsum += qm * b[k] / (1 + vfree[k] / vI) * (a[k] / (phia + a[k]) + omega * Ppr);
      rec = rsum * dx * dx;
      fprintf(ts, "%.2f,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.4f,%d,%.6e\n", t, Mc, Ms, Mm, neo, vmax,
              Tsum > 0 ? vt / Tsum : 0.0, Cp, Am, Ppr, rp, nsat, rec);
      if (operated && t_rec < 0 && (Ms + Mc) >= Mdet) { t_rec = t; fprintf(ev, "%.3f,recurrence,0,0,0\n", t); }
    }
    if (snapIdx < snaps.size() && t + 1e-9 >= snaps[snapIdx]) {
      char fn[512]; snprintf(fn, sizeof fn, "%s_snap_%04d.bin", out.c_str(), (int)std::lround(snaps[snapIdx]));
      FILE* f = fopen(fn, "wb"); int hdr[1] = {N}; fwrite(hdr, sizeof(int), 1, f);
      auto w = [&](const std::vector<double>& u) { std::vector<float> tmp(u.begin(), u.end()); fwrite(tmp.data(), sizeof(float), NN, f); };
      w(c); w(s); w(m); w(b); w(vfree); w(A); w(sig); fclose(f);
      snapIdx++;
    }
    if (step == nsteps) break;

    // ---- immune checkpoint blockade: reduces tumour-induced immune inactivation ----
    const bool ioOn = (t >= io_start && t < io_stop);
    const double bKt = ioOn ? bK * (1.0 - io_eff) : bK;
    const double kgain = ioOn ? (1.0 + io_gain) : 1.0;
    // ---- systemic priming ----
    double Mtot = Mc + Ms;
    Ppr += dt * (kP * Mtot / (Mtot + MP) - bP * Ppr);
    // ---- spatial update ----
#pragma omp parallel for schedule(static)
    for (int j = 0; j < N; ++j) {
      for (int i = 0; i < N; ++i) {
        int k = j * N + i;
        int kE = idx(i + 1, j), kW = idx(i - 1, j), kN = idx(i, j + 1), kS = idx(i, j - 1);
        auto lap = [&](const std::vector<double>& u) { return (u[kE] + u[kW] + u[kN] + u[kS] - 4 * u[k]) * inv; };
        // nonlinear (density-dependent) tumour diffusion: div(Dc*T*grad u)
        auto ndiff = [&](const std::vector<double>& u) {
          double TE = 0.5 * (Tn[k] + Tn[kE]), TW = 0.5 * (Tn[k] + Tn[kW]), TN = 0.5 * (Tn[k] + Tn[kN]), TS = 0.5 * (Tn[k] + Tn[kS]);
          return Dc * (TE * (u[kE] - u[k]) - TW * (u[k] - u[kW]) + TN * (u[kN] - u[k]) - TS * (u[k] - u[kS])) * inv;
        };
        double T = Tn[k], sg = sig[k], vf = vfree[k], G = Gam[k];
        double f = sg * sg / (th1 * th1 + sg * sg);
        double g = th2 * th2 / (th2 * th2 + sg * sg);
        double hyp = th1 * th1 / (th1 * th1 + sg * sg);
        double kill = kgain * (tau0 + tauA * G) * m[k] / (lamc + T);  // per-tumour-cell kill rate
        double grow = ac * f * (1 - T);
        c2[k] = (c[k] + dt * (ndiff(c) + grow * c[k])) / (1 + dt * (dc * g + kill));
        s2[k] = (s[k] + dt * (ndiff(s) + grow * s[k])) / (1 + dt * (dc * g + kill));
        // immune cells: diffusion, upwind chemotaxis, recruitment, losses
        auto flux = [&](int kk) {  // chemotactic flux from k toward neighbour
          double grad = (a[kk] - a[k]) / dx;
          double vel = chi * grad;
          return vel > 0 ? vel * m[k] : vel * m[kk];
        };
        double div_chem = (flux(kE) + flux(kW) + flux(kN) + flux(kS)) / dx;  // outward fluxes
        double Rm = qm * b[k] / (1 + vf / vI) * (a[k] / (phia + a[k]) + omega * Ppr);
        m2[k] = (m[k] + dt * (Dm * lap(m) - div_chem + Rm)) / (1 + dt * (bKt * T + bm));
        // immune attracting factor
        a2[k] = (a[k] + dt * (Da * lap(a) + gac * T + gam * G * m[k])) / (1 + dt * ba);
        // total VEGF (free + antibody-bound, rapid binding equilibrium)
        double thf = KD / (KD + A[k]);
        double prodV = T * (gv + av * hyp) + gvm * G * m[k];
        double lossV = bv * thf + bX * (1 - thf) + muv * b[k] * thf / (1 + vf);
        V2[k] = (V[k] + dt * (Dv * lap(V) + prodV)) / (1 + dt * lossV);
        // microvessel density
        double S = vf / (1 + vf);
        double bgrow = ab * b[k] * S * (1 - b[k] / bmax);
        double breg = db * (1 - S);
        b2[k] = (b[k] + dt * (Db * lap(b) + bgrow + breg)) / (1 + dt * breg);  // relaxes toward 1
        // tissue antibody
        A2[k] = (A[k] + dt * (DA * lap(A) + PA * b[k] * Cp)) / (1 + dt * (PA * b[k] + bA));
      }
    }
    // extinction cutoff: densities below one cell per grid node are removed
    if (step % outEvery == 0) {
      const double cut = 1.0 / cellsPerNode;
      for (int k = 0; k < NN; ++k) { if (c2[k] < cut) c2[k] = 0; if (s2[k] < cut) s2[k] = 0; }
    }
    std::swap(c, c2); std::swap(s, s2); std::swap(m, m2); std::swap(a, a2); std::swap(V, V2); std::swap(b, b2); std::swap(A, A2);
    Cp *= std::exp(-kel * dt);
  }
  fprintf(ev, "%.3f,end,0,0,%.3f\n", tend, t_rec);
  fclose(ts); fclose(ev);
  return 0;
}
