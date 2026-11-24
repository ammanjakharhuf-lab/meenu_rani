@@title Anti-angiogenic therapy combined with surgery: modelling VEGF blockade to prevent post-resection metastatic growth in melanoma

@@meta [Author names]

@@meta [Affiliations] · Corresponding author: [name, e-mail]

@@meta **Keywords:** melanoma; satellite metastasis; surgical resection; VEGF; bevacizumab; angiogenesis; tumour–immune interaction; reaction–diffusion model; pharmacokinetics

## Abstract

**Background.** Wide local excision is the primary treatment for localised cutaneous melanoma, yet some patients develop rapid recurrence in satellite and in-transit lesions that were dormant while the primary tumour was in place. One explanation is that the primary tumour sustains an immune response that also restrains nearby micrometastases, and that excision removes this control. Satellites that escape must then recruit their own blood supply, which suggests that blocking vascular endothelial growth factor (VEGF) after surgery could stop them growing.

**Methods.** We extended a spatial tumour–immune model of melanoma to a two-dimensional dermal sheet with stochastic satellite seeding, vessel-dependent oxygen supply and immune recruitment, VEGF-mediated suppression of immune-cell entry, and an anti-VEGF antibody described by plasma pharmacokinetics, tissue extravasation and rapid binding equilibrium. We simulated surgery alone, one year of adjuvant bevacizumab-like therapy (7.5 mg/kg every three weeks), continuous adjuvant therapy, and neoadjuvant-plus-adjuvant therapy. We ran 30 stochastic replicates per regimen for two tumour phenotypes: weak (A) and strong (B) VEGF-mediated immunosuppression. We also studied dose, duration, resection margin, parameter sensitivity and combination with an idealised immune checkpoint inhibitor.

**Results.** Excision triggered satellite regrowth in every replicate, with a median of 142 days to detectable disease in phenotype A. VEGF blockade did not delay detection, because early satellite growth was supported by co-opted native vessels. It did slow progression to major recurrence (median 605 versus 207 days in phenotype A; 525 versus 209 days in phenotype B). Once a one-year course washed out, tumour burden returned to the untreated trajectory. Only continued therapy kept 73% (A) and 60% (B) of replicates below the major-recurrence threshold for four years. In phenotype B, continuous therapy turned progressive disease into a controlled state with 33-fold lower final burden. The dose–response curve was flat across clinical doses, because tissue antibody exceeded the dissociation constant by more than two orders of magnitude. Neoadjuvant treatment shrank the primary tumour but narrowed the apparent tumour edge, which made narrow margins unsafe. Eradication of satellites required strengthening the immune response early after surgery, and adding anti-VEGF therapy never lowered the immune strength needed for cure.

**Conclusions.** In this model, VEGF blockade after excision slows satellite recurrence but cannot prevent it. Its benefit lasts only while the drug is present and is largest when the tumour relies on VEGF-driven immunosuppression. The results are consistent with the disease-free but not overall-survival benefit seen in the AVAST-M trial. They suggest that anti-angiogenic therapy would be most useful as maintenance or as a bridge to immune-based therapy, rather than as a short curative adjuvant course.

## 1. Introduction

Cutaneous melanoma causes most skin-cancer deaths, and its incidence continues to rise in many populations [@siegel2023]. Stage-specific survival is now well characterised [@gershenwald2017], and adjuvant immune checkpoint blockade has improved relapse-free survival after resection of high-risk disease [@weber2017]. Even so, recurrence after apparently complete excision remains a central clinical problem. A large share of these recurrences arise in the skin and subcutis near the scar, as satellite or in-transit metastases, rather than at distant sites.

Tumour growth beyond a few millimetres requires new blood vessels [@folkman1971]. The transition from a dormant, poorly vascularised lesion to an expanding, vascularised one, the "angiogenic switch", is driven mainly by VEGF [@hanahan1996; @hanahan2011; @ferrara2003]. In melanoma xenografts, constitutive VEGF expression predicts angiogenesis better than hypoxia-induced expression [@danielsen2000]. Local recurrences are often caused by growth of micro-satellites rather than by tumour left behind at the resection margin [@maccormack2004]. Case reports describe dormant satellites that grew explosively within weeks of excising a slowly growing primary lesion [@degiorgi2003]. More broadly, surgery itself can accelerate metastatic growth [@demicheli2008].

Several mechanisms could link removal of the primary tumour to metastatic escape. A primary tumour can release circulating angiogenesis inhibitors such as angiostatin and endostatin that keep distant lesions avascular [@oreilly1994; @oreilly1997]. In a reaction–diffusion model of melanoma, Eikenberry and colleagues proposed an alternative, immune-mediated mechanism [@eikenberry2009]. Immune cells recruited by the primary tumour suppress nearby micrometastases "in passing", and excision removes both these cells and the cytokines that recruit them. The released satellites can then grow faster than the original tumour. Enzyme-kinetic models of tumour dormancy reached related conclusions for growth-inhibitory factors [@boushaba2006].

If satellite escape after surgery depends on the angiogenic switch, then VEGF blockade is an obvious candidate to prevent it. Bevacizumab, a humanised anti-VEGF monoclonal antibody [@ferrara2004], improved survival in metastatic colorectal cancer [@hurwitz2004]. It was tested as adjuvant therapy for resected high-risk melanoma in the AVAST-M trial, which gave 7.5 mg/kg every three weeks for one year. Bevacizumab improved disease-free interval in the interim analysis [@corrie2014], but the final analysis showed no overall-survival benefit [@corrie2018]. Preclinical work also points to possible harms. Short-term anti-angiogenic treatment can accelerate metastasis [@ebos2009] and select for more invasive tumour behaviour [@paezribes2009]. Tumours can escape through alternative pro-angiogenic programmes [@bergers2008], and they can avoid sprouting angiogenesis entirely by co-opting pre-existing vessels [@kuczynski2019].

VEGF also acts on the immune system. Anti-angiogenic therapy can temporarily normalise tumour vessels [@jain2005]. Angiogenesis and immunosuppression share mediators [@motz2011], and VEGF inhibits dendritic-cell maturation [@gabrilovich1996]. Vessel-normalising doses of anti-angiogenic drugs reprogramme the immunosuppressive microenvironment and enhance immunotherapy [@huang2012; @fukumura2018]. In melanoma specifically, bevacizumab plus ipilimumab increased tumour infiltration by immune cells [@hodi2014]. Blocking VEGF after surgery could therefore act on two targets: the satellites' angiogenic switch, and the suppression of the immune response that controls them.

Mathematical models have been widely used to study angiogenesis-limited growth and anti-angiogenic treatment [@hahnfeldt1999; @anderson1998], tumour–immune dynamics [@kuznetsov1994; @depillis2005], and metastatic growth after surgery [@benzekry2016]. However, no model has combined surgical excision, satellite seeding, immune suppression of micrometastases, and the pharmacology of an anti-VEGF antibody in one spatial framework. Here we build such a model and ask four questions.

1. Can adjuvant VEGF blockade prevent, or only delay, satellite recurrence after excision?
2. How do dose, duration and timing (neoadjuvant versus adjuvant) shape the outcome?
3. Which tumour and immune properties decide whether blockade helps?
4. How does VEGF blockade interact with immune-strengthening therapy?

## 2. Methods

### 2.1 Model overview and geometry

We model a 40 × 40 mm sheet of dermis as a two-dimensional domain $\Omega$, centred on the primary tumour (@fig:schematic). The original model by Eikenberry et al. resolved depth in an axisymmetric cylinder, which forces every metastasis to be a ring around the primary tumour [@eikenberry2009]. Here we average over a 1-mm-thick layer so that satellites are discrete lesions at arbitrary positions. This approximation suits the lateral spread of satellites, which is the focus of this study, but not vertical invasion.

The state variables are listed in @tab:variables. Tumour cells are divided into the primary population $c$ and the satellite population $s$. Both are normalised to a carrying capacity of $K = 5\times10^{5}$ cells mm$^{-3}$ and share the total density

$$ T(\mathbf{x},t) = c(\mathbf{x},t) + s(\mathbf{x},t). $$ {#eq:total}

!fig[schematic](figures/fig1_schematic.png) Model structure and simulation set-up. (A) Interactions between primary tumour and satellite cells, VEGF, microvessels, immune effector cells, chemokine, systemic immune priming, and the anti-VEGF antibody. Arrows denote production or stimulation; red bars denote inhibition. (B) The 40 × 40 mm dermal sheet. Satellites are seeded at exponentially distributed distances from the edge of the primary tumour, and surgery removes everything within the tumour radius $r_p$ plus a margin $w$. Bottom: treatment timeline used in the simulations.

!table[variables] State variables of the model. Densities are dimensionless (normalised to the carrying capacity $K$ for cells, or to the half-saturation VEGF level $\varphi_v \approx 2$ ng mL$^{-1}$ for VEGF and antibody).
| Symbol | Quantity | Normalisation / units |
| $c$, $s$ | Primary-tumour and satellite cell density | fraction of $K = 5\times10^{5}$ cells mm$^{-3}$ |
| $b$ | Functional microvessel density | normal dermis $= 1$ |
| $\sigma$ | Tissue oxygen level (algebraic) | normal dermis $= 1$ |
| $V$, $v$ | Total and free (unbound) VEGF | units of $\varphi_v$ |
| $A$ | Tissue anti-VEGF antibody | units of $\varphi_v$ (molar equivalent) |
| $m$ | Cytotoxic immune effector cells | fraction of $K$ |
| $a$ | Immune-attracting chemokine | half-saturation level $= 1$ |
| $P(t)$ | Systemic immune priming (spatially uniform) | dimensionless, 0–1 |
| $C_p(t)$ | Plasma antibody concentration | units of $\varphi_v$; reported in µg mL$^{-1}$ |

The model rests on five main assumptions.

1. Tumour, immune and vascular populations are continuous densities. This is reasonable for lesions of more than about $10^{3}$ cells but not for single disseminated cells, which we handle with an extinction cut-off.
2. Oxygen is the growth-limiting resource and is set locally by perfusion. Nutrient gradients inside lesions smaller than the oxygen diffusion length are therefore ignored.
3. VEGF is the only angiogenic signal. Alternative factors such as bFGF, angiopoietins and IL-8 are absorbed into the constitutive rate $\gamma_v$ and are not blocked by the antibody.
4. All cytotoxic immune activity is represented by one effector population, which combines macrophages, NK cells and cytotoxic T cells. It needs perfused vessels to enter the tissue and is inactivated by contact with tumour cells.
5. The antibody acts only by neutralising VEGF. It has no direct cytotoxic or Fc-mediated effects.

Within these assumptions, the model contains the two mechanisms whose interaction we want to study: immune suppression of micrometastases by the primary tumour [@eikenberry2009], and the dependence of established lesions on VEGF-driven angiogenesis [@hanahan1996].

### 2.2 Oxygen supply and vessel co-option

Oxygen diffuses only 100–200 µm in tissue, much less than the millimetre scale of the lesions. We therefore treat oxygen as quasi-steady and set it by the local balance of vascular supply and consumption:

$$ \sigma = \frac{\kappa_n + b - 1}{\kappa_n + b - 1 + \lambda_\sigma T}. $$ {#eq:oxygen}

Normal dermis has $b = 1$ and $\sigma = 1$. Angiogenesis raises $b$ towards $b_{\mathrm{max}}$, and tumour cells consume oxygen in proportion to $\lambda_\sigma T$. The parameter $\kappa_n \in (0,1]$ is the share of native perfusion that tumour cells can use without new vessels, i.e. their capacity for vessel co-option [@kuczynski2019]. Because native dermal vessels already supply small, low-density lesions, satellites can grow to a substantial size before they need sprouting angiogenesis. Proliferation, hypoxic death and hypoxia-induced VEGF expression follow Hill functions:

$$ f(\sigma) = \frac{\sigma^{2}}{\theta_1^{2} + \sigma^{2}}, $$ {#eq:fsig}

$$ g(\sigma) = \frac{\theta_2^{2}}{\theta_2^{2} + \sigma^{2}}, $$ {#eq:gsig}

$$ h(\sigma) = \frac{\theta_1^{2}}{\theta_1^{2} + \sigma^{2}}. $$ {#eq:hsig}

### 2.3 Tumour cells and immune killing

Contact with tumour cells activates immune effector cells, with activation level

$$ \Gamma = \frac{T}{\xi + T}. $$ {#eq:activation}

Killing is limited by the number of immune cells. Each immune cell kills at most $\tau_0 + \tau_A \Gamma$ tumour cells per day [@eikenberry2009], so the per-capita kill rate of a tumour cell is

$$ k_{\mathrm{kill}}(m,T,t) = \left(1 + g_{\mathrm{IO}}(t)\right)\left(\tau_0 + \tau_A \Gamma\right)\frac{m}{\lambda_c + T}. $$ {#eq:kill}

The factor $1 + g_{\mathrm{IO}}(t)$ represents an idealised immune checkpoint inhibitor that raises cytotoxic capacity by a fraction $g_{\mathrm{IO}}$ while it is given, and equals 1 otherwise. Tumour cells move by density-dependent diffusion [@eikenberry2009], proliferate logistically with oxygen-dependent rate, die under hypoxia, and are killed by immune cells:

$$ \frac{\partial c}{\partial t} = \nabla\cdot\left(D_c T \nabla c\right) + \alpha_c f(\sigma)(1 - T)c - \delta_c g(\sigma) c - k_{\mathrm{kill}} c, $$ {#eq:primary}

$$ \frac{\partial s}{\partial t} = \nabla\cdot\left(D_c T \nabla s\right) + \alpha_c f(\sigma)(1 - T)s - \delta_c g(\sigma) s - k_{\mathrm{kill}} s. $$ {#eq:satellite}

Primary and satellite cells follow identical kinetics. Labelling them separately only lets us attribute burden and apply surgery to the primary tumour. Densities below one cell per grid node are set to zero once per simulated day, which allows complete extinction in the continuum model.

### 2.4 VEGF, antibody binding and microvessels

Bevacizumab binds VEGF with nanomolar-order affinity [@ferrara2004], much faster than the days-long time scales of growth. We therefore assume rapid binding equilibrium. The unbound fraction $\theta_f$ and the free VEGF concentration $v$ follow from the total VEGF $V$ and tissue antibody $A$:

$$ \theta_f = \frac{K_D}{K_D + A}, \qquad v = \theta_f V. $$ {#eq:binding}

This form assumes that the antibody is in large excess over VEGF ($A \gg V$), which holds by about four orders of magnitude at clinical doses (Section 3.3). Total VEGF is produced by tumour cells (constitutively and in response to hypoxia [@danielsen2000]) and by activated immune cells [@nesbit2001]. It diffuses, free VEGF is degraded or taken up by endothelium, and antibody-bound VEGF is cleared more slowly:

$$ \frac{\partial V}{\partial t} = D_v \nabla^{2}V + T\left(\gamma_v + \alpha_v h(\sigma)\right) + \gamma_{vm}\Gamma m - \left[\beta_v \theta_f + \beta_X(1 - \theta_f)\right]V - \mu_v b\frac{v}{1 + v}. $$ {#eq:vegf}

Free VEGF stimulates endothelial sprouting through the saturating response $S(v) = v/(1+v)$. When VEGF is scarce, new vessels regress towards the native density [@jain2005]:

$$ \frac{\partial b}{\partial t} = D_b \nabla^{2}b + \alpha_b b S(v)\left(1 - \frac{b}{b_{\mathrm{max}}}\right) - \delta_b\left(1 - S(v)\right)(b - 1). $$ {#eq:vessels}

### 2.5 Immune cells, chemokine and systemic priming

Effector cells reach the tissue through perfused vessels, so recruitment scales with $b$. VEGF makes the endothelium anergic and lowers immune-cell entry [@motz2011; @gabrilovich1996], which we represent with the factor

$$ \psi(v) = \frac{1}{1 + v/v_I}. $$ {#eq:anergy}

The parameter $v_I$ sets how strongly VEGF suppresses recruitment: a small $v_I$ means strong suppression. Recruitment combines local homing to the chemokine $a$ with influx of effector cells primed systemically by the tumour, $P(t)$:

$$ R_m = q_m b \psi(v)\left[\frac{a}{\varphi_a + a} + \omega P(t)\right]. $$ {#eq:recruit}

Immune cells diffuse, move up chemokine gradients, are inactivated by tumour cells (rate $\beta_K$, representing the immunosuppressive microenvironment), and turn over:

$$ \frac{\partial m}{\partial t} = D_m \nabla^{2}m - \chi_m \nabla\cdot\left(m\nabla a\right) + R_m - \beta_K T m - \beta_m m, $$ {#eq:immune}

$$ \frac{\partial a}{\partial t} = D_a \nabla^{2}a + \gamma_{ac}T + \gamma_{am}\Gamma m - \beta_a a. $$ {#eq:chemokine}

Systemic priming rises with total tumour burden $M(t)$ and decays with rate $\beta_P$ once the antigen source is removed:

$$ \frac{dP}{dt} = k_P \frac{M}{M + M_P} - \beta_P P, $$ {#eq:priming}

$$ M(t) = M_c + M_s = K H\int_{\Omega}\left(c + s\right)d\mathbf{x}, $$ {#eq:burden}

where $H = 1$ mm is the thickness of the dermal layer represented.

### 2.6 Antibody pharmacokinetics and tissue delivery

Plasma antibody follows one-compartment kinetics with intravenous boluses of size $C_0\phi_d$ at dosing times $t_k$. Here $\phi_d$ is the dose as a fraction of 7.5 mg/kg:

$$ \frac{dC_p}{dt} = -k_{\mathrm{el}}C_p + C_0\phi_d\sum_{k}\delta(t - t_k), $$ {#eq:pk}

$$ k_{\mathrm{el}} = \frac{\ln 2}{t_{1/2}}, $$ {#eq:kel}

with solution

$$ C_p(t) = C_0\phi_d\sum_{t_k \le t}e^{-k_{\mathrm{el}}(t - t_k)}. $$ {#eq:pksol}

With a terminal half-life of about 20 days [@lu2008] and dosing every $\Delta = 21$ days, drug accumulates by the factor

$$ R_{\mathrm{acc}} = \frac{1}{1 - e^{-k_{\mathrm{el}}\Delta}} \approx 1.93, $$ {#eq:accum}

so plasma concentrations oscillate between about $C_0 R_{\mathrm{acc}}e^{-k_{\mathrm{el}}\Delta}$ and $C_0 R_{\mathrm{acc}}$ at steady state. We take $C_0$ = 175 µg mL$^{-1}$, a 525-mg dose in about 3 L of plasma. The antibody leaves the blood through perfused vessels, so delivery scales with $b$. It also diffuses slowly and is cleared from the tissue:

$$ \frac{\partial A}{\partial t} = D_A \nabla^{2}A + P_A b\left(C_p - A\right) - \beta_A A. $$ {#eq:tissuedrug}

The fraction of VEGF neutralised at any location is then

$$ \phi_N = 1 - \theta_f = \frac{A}{K_D + A}. $$ {#eq:neutral}

### 2.7 Surgery, metastatic seeding and outcomes

Surgery at $t_s = 365$ days resets all fields to their tumour-free values inside the excision disc:

$$ u(\mathbf{x}, t_s^{+}) = u_0 \quad \text{for} \quad \left|\mathbf{x} - \mathbf{x}_0\right| \le r_p + w, $$ {#eq:surgery}

where $u_0$ denotes $c = s = V = m = a = 0$ and $b = 1$. The clinically visible radius $r_p$ is taken as the radius of a disc with the same area as the region where $c > 0.05$, and $w$ is the margin (2 mm at baseline). Before surgery, satellites are seeded as a Poisson process whose intensity is proportional to primary-tumour burden:

$$ \lambda(t) = \lambda_{\mathrm{seed}}\frac{M_c(t)}{M_{\mathrm{ref}}}. $$ {#eq:seedrate}

Each seed lands at a uniformly distributed angle. Its distance $d$ beyond the visible edge is exponentially distributed:

$$ p(d) = \lambda_d e^{-\lambda_d d}, $$ {#eq:seeddist}

and it adds a small Gaussian lesion of about $10^{3}$ cells centred at $\mathbf{x}_k$:

$$ s(\mathbf{x}) \leftarrow s(\mathbf{x}) + s_0\exp\left(-\frac{\left|\mathbf{x} - \mathbf{x}_k\right|^{2}}{2w_s^{2}}\right). $$ {#eq:seed}

With baseline parameters, a mean of 26 satellites (phenotype A) to 52 satellites (phenotype B) were seeded during the first year. Recurrence time is the first post-operative time at which total burden exceeds a threshold:

$$ t_{\mathrm{rec}} = \inf\left\{t > t_s : M(t) \ge M_{\mathrm{thr}}\right\} - t_s. $$ {#eq:trec}

We used two thresholds. Detectable recurrence is $M_{\mathrm{thr}} = 10^{6}$ cells, roughly a 1–2 mm nodule. Major recurrence is $M_{\mathrm{thr}} = 10^{7}$ cells, comparable to the primary tumour at the time of surgery. Cumulative post-operative tumour exposure is

$$ \mathrm{AUC} = \int_{t_s}^{t_{\mathrm{end}}}M(t)\,dt, $$ {#eq:auc}

with $t_{\mathrm{end}}$ = 1825 days, i.e. four years after surgery. Event-free fractions across stochastic replicates were estimated with the Kaplan–Meier product-limit estimator, with administrative censoring at $t_{\mathrm{end}}$:

$$ \hat{S}(t) = \prod_{t_i \le t}\left(1 - \frac{d_i}{n_i}\right), $$ {#eq:km}

where $d_i$ events occur at time $t_i$ among $n_i$ replicates at risk. The benefit of a regimen relative to surgery alone is summarised as the relative reduction in AUC:

$$ E = 1 - \frac{\mathrm{AUC}_{\mathrm{treated}}}{\mathrm{AUC}_{\mathrm{surgery}}}. $$ {#eq:benefit}

### 2.8 Dormancy condition for a micrometastasis

Linearising @eq:satellite about a newly seeded satellite in normal tissue ($T \to 0$, $b = 1$, $\sigma = 1$, $\Gamma \to 0$) shows that the satellite stays dormant when the local immune-cell density exceeds a threshold:

$$ m > m^{*} = \frac{\lambda_c\left[\alpha_c f(1) - \delta_c g(1)\right]}{\left(1 + g_{\mathrm{IO}}\right)\tau_0}. $$ {#eq:dormancy}

At baseline $m^{*} \approx 0.013$, about $6\times10^{3}$ effector cells mm$^{-3}$. VEGF does not appear in @eq:dormancy. Anti-VEGF therapy can affect a micrometastasis only indirectly, by changing immune recruitment through $b$ and $\psi(v)$ in @eq:recruit, or once the lesion is large enough to become hypoxic.

### 2.9 Parameters, phenotypes and regimens

Parameter values are listed in @tab:params. Where possible they follow the ranges compiled by Eikenberry et al. [@eikenberry2009], who based them on melanoma doubling times, VEGF transport and macrophage kill rates. Antibody parameters follow published bevacizumab pharmacokinetics [@lu2008; @ferrara2004]. Immune recruitment, priming and co-option parameters are poorly constrained. We calibrated them so that, as in the original model, the untreated primary tumour reaches an immune-limited quasi-steady state and nearby satellites are suppressed. We then tested them in the sensitivity analysis.

We compare two phenotypes that differ only in VEGF-mediated suppression of immune recruitment. Phenotype A has weak suppression ($v_I = 1$). Phenotype B has strong suppression ($v_I = 0.1$), consistent with the immunosuppressive VEGF environment of many melanomas [@motz2011; @gabrilovich1996]. The treatment regimens are listed in @tab:regimens. Adjuvant therapy starts 28 days after surgery to allow wound healing, as in clinical practice.

!table[params] Baseline parameter values. Time in days, space in mm. "Calibrated" marks parameters chosen to reproduce immune-limited quasi-steady growth of the primary tumour and suppression of nearby satellites; these were varied in the sensitivity analysis.
| Parameter | Meaning | Value | Source |
| $\alpha_c$, $\delta_c$ | Maximal proliferation and hypoxic death rate | 0.35, 0.35 day$^{-1}$ | doubling time 1–4 days [@eikenberry2009] |
| $D_c$ | Density-dependent tumour motility | 0.02 mm$^{2}$ day$^{-1}$ | [@eikenberry2009] |
| $\theta_1$, $\theta_2$ | Oxygen half-saturation (growth, death) | 0.5, 0.3 | scaled from [@eikenberry2009] |
| $\lambda_\sigma$, $\kappa_n$ | Oxygen demand; co-option capacity | 6, 1 | calibrated |
| $\tau_0$, $\tau_A$ | Kill capacity, inactive / activated | 0.2, 2.0 cells IC$^{-1}$ day$^{-1}$ | macrophage data via [@eikenberry2009] |
| $\lambda_c$, $\xi$ | Kill saturation; activation half-density | 0.01, 0.05 | [@eikenberry2009] |
| $q_m$, $\omega$ | Vessel-dependent recruitment; primed-influx weight | 0.001 day$^{-1}$, 0.5 | calibrated |
| $\beta_K$, $\beta_m$ | Tumour-induced inactivation; turnover | 0.3, 0.02 day$^{-1}$ | [@eikenberry2009] |
| $D_m$, $\chi_m$ | Immune diffusion; chemotaxis | 0.05, 0.05 mm$^{2}$ day$^{-1}$ | [@eikenberry2009] |
| $D_a$, $\beta_a$, $\gamma_{ac}$, $\gamma_{am}$ | Chemokine diffusion, decay, production | 1.5, 5, 5, 20 | MCP-1 data via [@eikenberry2009] |
| $k_P$, $M_P$, $\beta_P$ | Systemic priming rate, half-burden, decay | 0.02 day$^{-1}$, $5\times10^{6}$ cells, 0.02 day$^{-1}$ | calibrated |
| $v_I$ | VEGF level halving immune recruitment | 1 (A) or 0.1 (B) | phenotype parameter |
| $D_v$, $\beta_v$ | VEGF diffusion and degradation | 0.5 mm$^{2}$ day$^{-1}$, 20 day$^{-1}$ | [@eikenberry2009] |
| $\gamma_v$, $\alpha_v$, $\gamma_{vm}$ | Constitutive, hypoxic, immune-cell VEGF production | 20, 30, 20 day$^{-1}$ | [@danielsen2000; @eikenberry2009] |
| $\beta_X$, $\mu_v$ | Bound-VEGF clearance; endothelial uptake | 1, 2 day$^{-1}$ | assumed |
| $\alpha_b$, $\delta_b$, $b_{\mathrm{max}}$, $D_b$ | Sprouting, regression, maximal density, motility | 0.3, 0.1 day$^{-1}$, 4, 0.01 | [@eikenberry2009] |
| $K_D$ | Antibody–VEGF dissociation constant | 23 $\varphi_v$ (≈1 nM) | nanomolar order [@ferrara2004] |
| $t_{1/2}$, $C_0$ | Plasma half-life; peak per 7.5 mg/kg dose | 20 days; 175 µg mL$^{-1}$ | [@lu2008] |
| $P_A$, $\beta_A$, $D_A$ | Extravasation, tissue clearance, diffusion | 0.02, 0.03 day$^{-1}$, 0.1 mm$^{2}$ day$^{-1}$ | assumed (IgG) |
| $\lambda_{\mathrm{seed}}$, $M_{\mathrm{ref}}$, $1/\lambda_d$ | Seeding rate, reference burden, mean seed distance | 0.08 day$^{-1}$, $10^{7}$ cells, 3 mm | calibrated |
| $w$, $t_s$ | Resection margin; time of surgery | 2 mm; day 365 | baseline |

!table[regimens] Simulated treatment regimens. Anti-VEGF doses are 7.5 mg/kg every 21 days, as in AVAST-M [@corrie2014].
| Code | Regimen | Anti-VEGF schedule |
| R0 | No treatment | none |
| R1 | Surgery alone | none |
| R2 | Surgery + 1-year adjuvant anti-VEGF | days 393–758 (18 doses) |
| R3 | Surgery + continuous adjuvant anti-VEGF | day 393 to end of simulation |
| R4 | Neoadjuvant + 1-year adjuvant | days 302–758 (3 doses before surgery, gap for surgery) |

### 2.10 Numerical methods

The equations were discretised on a uniform 81 × 81 grid ($\Delta x$ = 0.5 mm) with no-flux boundaries. Diffusion used second-order central differences, density-dependent tumour diffusion used face-averaged coefficients, and chemotaxis used a first-order upwind flux. Time stepping was semi-implicit, with production terms treated explicitly and linear loss terms implicitly:

$$ u^{n+1} = \frac{u^{n} + \Delta t\left(L_h u^{n} + \Pi^{n}\right)}{1 + \Delta t\Lambda^{n}}, $$ {#eq:scheme}

where $L_h$ is the discrete transport operator, and $\Pi^{n}$ and $\Lambda^{n}$ are the production and per-capita loss rates at step $n$. With $\Delta t$ = 0.02 days, the explicit diffusion stability limit $\Delta t \le \Delta x^{2}/(4D_{\mathrm{max}})$ is met for the fastest species, the chemokine, by a factor of two. The solver is written in C++. Thirty independent random seeds were used for each regimen and phenotype. Within a seed, random numbers are shared across regimens, so regimens with identical pre-operative histories have identical satellites at the time of surgery. All analysis and figure scripts use only the Python standard library and are provided with the source code.

## 3. Results

### 3.1 Excision releases satellites from immune control

Without treatment, the primary tumour in phenotype A grew for about four months, became vascularised, and then settled into an immune-limited quasi-steady state of about $1.0\times10^{7}$ cells (radius about 5 mm; @fig:burden A, R0). During the first year, 19 satellites were seeded in the representative simulation. Together they never exceeded $5\times10^{4}$ cells and totalled only $2.9\times10^{3}$ cells at surgery, held by the effector cells drawn in by the primary tumour and by systemic priming.

Excision with a 2-mm margin (radius 7.15 mm) removed the primary tumour and 9 of the 19 satellites. The other ten, which had been dormant, then escaped (@fig:snapshots A). Two processes removed their immune control. First, excision removed the chemokine source. Second, systemic priming decayed with a half-life of $\ln 2/\beta_P \approx 35$ days. Together these lowered vessel-dependent immune recruitment to below 10% of its pre-operative level within about 140 days of surgery (@fig:pkpd D shows phenotype B, which behaves the same way). The satellites reached detectable size 163 days after surgery and major recurrence after 234 days. Their total mass peaked at $1.67\times10^{7}$ cells, 1.6 times the mass of the excised primary tumour (@fig:burden A, R1). This reproduces the central result of the original axisymmetric model [@eikenberry2009] with discrete rather than ring-shaped satellites. The regrowing satellites eventually re-stimulated immunity, and the system returned to a quasi-steady state of $8.6\times10^{6}$ cells spread over several lesions.

The spatial pattern of recurrence (@fig:snapshots A–B) explains why burden can exceed that of the primary tumour. Before surgery, satellites close to the primary tumour sat within its immune halo and stayed at densities too low to see on the colour scale. Within about five months of excision, several satellites had grown into separate nodules, each of which crossed the angiogenic threshold and became vascularised ($b \approx 2.5$). Because each nodule grows outwards from its own centre, total growing surface, and hence growth rate, rises with the number of escaped lesions. Recurrence therefore spreads over a wider area than the original tumour, as seen in the clinical case that motivated the original model [@degiorgi2003]. Satellites that landed inside the excision disc were removed with the primary tumour. This is why the margin experiments below show a modest dependence of recurrence on margin width.

In phenotype B, VEGF-driven suppression of recruitment allowed a larger primary tumour ($3.8\times10^{7}$ cells at surgery) and seeding of more satellites (51 in the representative run). After excision, the satellites did not reach a steady state. Burden rose for the full four years to $2.6\times10^{8}$ cells (@fig:burden B). This exceeded the untreated trajectory, in which the primary tumour reached $2.1\times10^{8}$ cells, because several regrowing lesions expanded in parallel.

!fig[burden](figures/fig3_burden.png) Total tumour burden (primary plus satellites) for the representative simulation (seed 1) in phenotype A (weak VEGF-mediated immunosuppression) and phenotype B (strong). The vertical dashed line marks surgery on day 365 and the shaded band the one-year adjuvant course. Horizontal dotted lines mark the detectable-recurrence ($10^{6}$ cells) and major-recurrence ($10^{7}$ cells) thresholds. In phenotype A, VEGF blockade lowers the post-operative peak but not the long-term state unless continued. In phenotype B, only continuous therapy prevents progressive growth.

!fig[snapshots](figures/fig2_snapshots.png) Spatial dynamics of recurrence in phenotype A (representative run). Columns show the central 30 × 30 mm of the domain on days 364 (just before surgery), 450, 520, 600 and 750. (A, B) Surgery alone: satellites outside the excision disc escape, recruit new vessels ($b > 1$) and grow into vascularised nodules. (C, D) One year of adjuvant anti-VEGF: the same satellites still grow, but at lower density, and no new vessels form while the drug is present. Regrowth is supported by co-opted native vessels.

### 3.2 VEGF blockade slows but does not prevent recurrence

Adjuvant VEGF blockade changed how satellites grew, not whether they grew. During therapy no neovasculature formed (@fig:snapshots D; @fig:pkpd C), but satellites still expanded at intermediate density using native vessels (@fig:snapshots C). Their early, co-option-supported growth was almost unaffected. In the representative phenotype-A run, detection came 167 days after surgery with one year of therapy, versus 163 days with surgery alone. What therapy did limit was the later phase that requires angiogenesis. The post-operative peak fell from $1.67\times10^{7}$ to $9.9\times10^{6}$ cells (−41%), and this run never crossed the major-recurrence threshold. After the drug washed out, satellites revascularised, and the system returned to the same quasi-steady burden as surgery alone ($8.6\times10^{6}$ cells; @fig:burden A). The one-year course therefore reduced cumulative exposure by only 14%. Continuous therapy kept vessels at native density and held burden at $5.3\times10^{6}$ cells, a 38% lower steady state with a 40% reduction in AUC.

The 30 stochastic replicates confirmed this pattern (@fig:km; @tab:outcomes). Satellite seeds varied in number and position, but detectable recurrence occurred in every replicate of every regimen in phenotype A. Median time to detection was 142 days with surgery alone and 144 days with one year of adjuvant therapy. The difference lay in progression to major recurrence: the median was 207 days with surgery alone, 605 days with one-year therapy, and not reached with continuous therapy. The one-year course mainly shifted the major-recurrence curve to the right by about the length of treatment plus washout (@fig:km B). Only 7% of replicates remained free of major recurrence at four years, versus 73% with continuous therapy.

!fig[km](figures/fig5_km.png) Event-free fractions across 30 stochastic replicates per regimen. (A, C) Detectable recurrence ($\ge 10^{6}$ cells) is not delayed by any anti-VEGF regimen. (B, D) Major recurrence ($\ge 10^{7}$ cells) is delayed by one-year adjuvant therapy roughly by the duration of treatment, and prevented in most replicates only by continuous therapy. In phenotype B, events at time zero are replicates in which satellites outside the excision disc exceeded the threshold within days of surgery.

!table[outcomes] Outcomes across 30 stochastic replicates per regimen. Times are days after surgery (median; NR = not reached). Burdens are means ± SD over replicates. Event-free fractions are at four years after surgery.
| Phenotype | Regimen | Median time to detection | Median time to major recurrence | Free of major recurrence | Post-operative peak (cells) | Burden at day 1825 (cells) | AUC change vs R1 |
| A | R1 Surgery alone | 142 | 207 | 0% | $1.66\times10^{7}$ ± $3.4\times10^{6}$ | $8.7\times10^{6}$ | — |
| A | R2 1-yr adjuvant | 144 | 605 | 7% | $1.09\times10^{7}$ ± $6.2\times10^{5}$ | $8.7\times10^{6}$ | −13% |
| A | R3 Continuous | 144 | NR | 73% | $8.9\times10^{6}$ ± $1.6\times10^{6}$ | $5.3\times10^{6}$ | −41% |
| A | R4 Neoadjuvant + adjuvant | 124 | 608 | 10% | $1.08\times10^{7}$ ± $4.7\times10^{5}$ | $8.6\times10^{6}$ | −12% |
| B | R1 Surgery alone | 160 | 209 | 3% | $1.84\times10^{8}$ ± $6.4\times10^{7}$ | $1.8\times10^{8}$ | — |
| B | R2 1-yr adjuvant | 162 | 525 | 3% | $1.16\times10^{8}$ ± $3.1\times10^{7}$ | $1.2\times10^{8}$ | −52% |
| B | R3 Continuous | 162 | NR | 60% | $9.4\times10^{6}$ ± $3.1\times10^{6}$ | $5.5\times10^{6}$ | −94% |
| B | R4 Neoadjuvant + adjuvant | 142 | 508 | 0% | $1.17\times10^{8}$ ± $1.7\times10^{7}$ | $1.2\times10^{8}$ | −51% |

VEGF blockade helped more in phenotype B, where VEGF both drives angiogenesis and suppresses immune entry. One year of therapy halved cumulative exposure (−52%). Continuous therapy turned progressive disease into a controlled state of $5.5\times10^{6}$ cells, 33-fold below surgery alone, and kept 60% of replicates below the major-recurrence threshold. In 12 of the 30 phenotype-B replicates, satellites left outside the excision disc exceeded $10^{6}$ cells within a week of surgery, and in 3 they exceeded $10^{7}$ cells. These appear as events at time zero in @fig:km C–D. They represent clinically occult in-transit disease that no adjuvant regimen could undo.

### 3.3 Pharmacology: saturation and washout

At 7.5 mg/kg every 21 days, simulated plasma antibody reached a steady state between about 165 and 330 µg mL$^{-1}$ (@fig:pkpd A), matching the accumulation predicted by @eq:accum. Tissue antibody exceeded $K_D$ by more than two orders of magnitude. Free VEGF in tumour tissue therefore fell by about 99% (from 0.60 to 0.006 $\varphi_v$ in phenotype B; @fig:pkpd B), while total VEGF accumulated in bound form. When a one-year course ended on day 758, plasma levels fell to about 10 µg mL$^{-1}$ by day 850 and 2 µg mL$^{-1}$ by day 900. Free VEGF rose correspondingly from 0.005 to 0.15 $\varphi_v$, and sprouting resumed within about 100–150 days of the last dose (@fig:pkpd C). We saw no overshoot of free VEGF above untreated levels after washout. Regrowth after withdrawal reflected the resumption of angiogenesis by satellites that had kept growing on co-opted vessels, not a VEGF rebound.

!fig[pkpd](figures/fig4_pkpd.png) Pharmacokinetics and pharmacodynamics in phenotype B (representative run). (A) Plasma antibody concentration for one-year and continuous adjuvant therapy. (B) Mean free VEGF within tumour tissue. (C) Total neovascular area. (D) Total vessel-dependent immune recruitment, @eq:recruit, integrated over the domain. Recruitment falls sharply after excision because the chemokine source is removed and systemic priming decays.

Because tissue antibody is far in excess, the response is saturated. Continuous therapy at 10% of the clinical dose was almost as effective as the full dose in both phenotypes (@fig:dose A). In phenotype B, burden at day 1825 was $1.0\times10^{7}$ cells at 10% dose versus $5.7\times10^{6}$ at full dose. At 1% of the clinical dose, the effect was largely lost ($1.5\times10^{8}$ cells). In line with this, changing $K_D$ by ±50% did not change the outcome (@fig:sensitivity). Duration, not dose, decided the benefit (@fig:dose B). In phenotype B, burden at day 1825 fell steadily as adjuvant therapy was extended from 0 to 3, 6, 12, 24 and 36 months ($2.6\times10^{8}$, $2.6\times10^{8}$, $2.4\times10^{8}$, $1.6\times10^{8}$, $8.0\times10^{7}$ and $3.3\times10^{7}$ cells). Only therapy maintained to the end of the simulation held the tumour at the controlled level. In phenotype A, any finite course led to the same long-term steady state. Longer courses only lowered the transient post-operative peak, from $1.67\times10^{7}$ cells without treatment to $9.3\times10^{6}$ cells with 24 months of therapy.

!fig[dose](figures/fig6_dose_duration.png) Dose and duration. (A) Tumour burden at day 1825 under continuous adjuvant therapy as a function of dose, expressed as a fraction of 7.5 mg/kg every three weeks. Dashed lines mark surgery alone. The response is saturated above about 10% of the clinical dose. (B) Burden at day 1825 (solid) and post-operative peak burden (dashed) as functions of adjuvant duration. The 48-month course covers the whole simulated follow-up.

### 3.4 Neoadjuvant therapy and resection margins

Three doses before surgery reduced primary-tumour burden at the time of excision by about 65% ($3.2\times10^{6}$ versus $9.3\times10^{6}$ cells, mean over replicates), and the number of satellites seeded fell slightly (24 versus 26). However, therapy lowered tumour density more than it shrank the tumour's footprint. The contour $c > 0.05$ used to set the clinical margin pulled inwards and left low-density tumour cells near the edge. As a result, fewer seeded satellites fell inside the excision disc (8.8 versus 13.2), and detectable recurrence came earlier (median 124 versus 144 days; @tab:outcomes). The margin experiment (@tab:margins) showed the danger directly. With a 1-mm margin, surgery alone removed all primary-tumour cells, but after neoadjuvant therapy residual tumour at the excision edge regrew to $8.0\times10^{6}$ cells, i.e. local persistence. Margins of 2 mm or more were safe in both cases. Widening the margin beyond 2 mm removed more satellites (12 of 19 at 4 mm versus 9 at 2 mm) but barely changed the peak or long-term burden, because the remaining satellites were enough to cause recurrence.

!table[margins] Effect of resection margin $w$ in phenotype A (representative run). "Residual primary" is the primary-tumour burden at day 1825; non-zero values indicate local persistence at the excision edge.
| Margin $w$ (mm) | Regimen | Satellites removed | Time to detection (days) | Post-operative peak (cells) | Residual primary at day 1825 (cells) |
| 0.5 | Surgery alone | 2 / 19 | 128 | $2.5\times10^{7}$ | $5.6\times10^{6}$ |
| 0.5 | Neoadjuvant + adjuvant | 0 / 17 | 101 | $1.4\times10^{7}$ | $8.7\times10^{6}$ |
| 1 | Surgery alone | 4 / 19 | 148 | $1.7\times10^{7}$ | 0 |
| 1 | Neoadjuvant + adjuvant | 1 / 17 | 107 | $1.2\times10^{7}$ | $8.0\times10^{6}$ |
| 2 | Surgery alone | 9 / 19 | 163 | $1.7\times10^{7}$ | 0 |
| 2 | Neoadjuvant + adjuvant | 6 / 17 | 144 | $1.0\times10^{7}$ | 0 |
| 4 | Surgery alone | 12 / 19 | 161 | $1.6\times10^{7}$ | 0 |
| 4 | Neoadjuvant + adjuvant | 11 / 17 | 142 | $1.0\times10^{7}$ | 0 |

### 3.5 Which properties determine benefit?

One-at-a-time sensitivity analysis (each parameter ×0.5 and ×1.5) showed that the benefit of continuous therapy, @eq:benefit, depended mostly on the tumour–immune balance and hardly at all on drug parameters (@fig:sensitivity). The baseline benefit was a 40% reduction in AUC. Benefit grew when immune control was weaker: lower recruitment $q_m$ (58%), lower kill capacity $\tau_A$ (73%), faster loss of priming $\beta_P$ (74%), or faster proliferation $\alpha_c$ (72%). When recruitment was 50% stronger, benefit disappeared and therapy became slightly harmful (−3%), because the immune system already controlled the satellites and fewer vessels meant fewer recruited effector cells. Lower oxygen demand ($\lambda_\sigma \times 0.5$) produced larger, more vascularised recurrences and raised the benefit to 84%. Higher constitutive VEGF production also raised it (57%). Slower proliferation ($\alpha_c \times 0.5$) almost abolished the benefit (3%), because satellites then stayed small enough for the immune system to control. Lowering co-option capacity $\kappa_n$ by half changed the benefit little (38%) but brought recurrence forward: the smaller primary tumour was excised with a smaller disc, which left 10 of 11 satellites outside it. With $\beta_P \times 0.5$, the primary tumour was eradicated by the immune system before surgery, so no benefit could be defined.

!fig[sensitivity](figures/fig7_sensitivity.png) One-at-a-time sensitivity of the benefit of continuous adjuvant anti-VEGF therapy (relative reduction in post-operative AUC, @eq:benefit) in phenotype A. Bars show the benefit when each parameter is halved (blue) or increased by 50% (red), relative to the baseline benefit of 40% (vertical line). Missing bars indicate values that are not meaningful: $\kappa_n$ cannot exceed 1, and $\beta_P \times 0.5$ eradicates the primary tumour before surgery.

### 3.6 VEGF blockade with immune-strengthening therapy

Because @eq:dormancy places the decision between dormancy and escape in the immune compartment, we tested an idealised checkpoint inhibitor that raised kill capacity by a fraction $g_{\mathrm{IO}}$ for one year, starting 28 days after surgery (@fig:combination; @tab:combination). In phenotype A, $g_{\mathrm{IO}} \ge 0.75$ eliminated all satellites, while weaker blockade only delayed recurrence. In phenotype B, where immune suppression is the main obstacle, $g_{\mathrm{IO}} = 0.25$ was already enough for cure. Adding one year of anti-VEGF therapy never lowered the $g_{\mathrm{IO}}$ needed for cure. At sub-curative strengths in phenotype A, it was mildly antagonistic. With $g_{\mathrm{IO}} = 0.25$, checkpoint blockade alone kept the representative run below the major-recurrence threshold, but adding anti-VEGF therapy allowed major recurrence at 604 days. The post-operative peak rose by 15–26% for $g_{\mathrm{IO}}$ between 0.25 and 0.6. The cause was reduced vessel density, which lowered effector recruitment, @eq:recruit, during the period when the satellites were immune-controlled but not yet eliminated. Timing mattered more than the drug combination. We delayed the start of one year of blockade ($g_{\mathrm{IO}} = 1$) to 115, 175 or 235 days after surgery, by which time satellite burden had grown from about $3\times10^{4}$ to more than $10^{7}$ cells. No delayed regimen eliminated the satellites, with or without anti-VEGF therapy, and the long-term burden settled at 7–8 × $10^{6}$ cells. Starting at 115 or 175 days delayed major recurrence to about 500 and 610–640 days. Starting at 235 days came too late to prevent the first major recurrence (234 days) when checkpoint blockade was given alone. With adjuvant anti-VEGF therapy already running, major recurrence was instead delayed to 640 days, because the antibody had slowed the angiogenic phase until the immune treatment began.

!fig[combination](figures/fig8_combination.png) Combination with an idealised checkpoint inhibitor given for one year from day 393. Post-operative AUC (floored at $10^{3}$ cell·days for display) as a function of the kill-capacity gain $g_{\mathrm{IO}}$, with and without one year of adjuvant anti-VEGF therapy. Cure corresponds to the collapse of AUC to the residual micrometastatic level. Anti-VEGF therapy does not lower the cure threshold in either phenotype.

!table[combination] Combination with checkpoint blockade (representative runs). "Cure" means all tumour cells were eliminated before day 1825.
| Phenotype | $g_{\mathrm{IO}}$ | Checkpoint alone: time to major recurrence / outcome | With 1-yr anti-VEGF: time to major recurrence / outcome |
| A | 0 | 234 d / steady state | NR / steady state |
| A | 0.25 | NR / steady state | 604 d / steady state |
| A | 0.5 | NR / steady state | 579 d / steady state |
| A | 0.75 | cure | cure |
| A | 1.0 | cure | cure |
| B | 0 | 238 d / progressive | 295 d / progressive |
| B | 0.25 | cure | cure |
| B | 1.0 | cure | cure |

## 4. Discussion

We asked whether VEGF blockade after excision can stop satellite metastases from growing once the immune control provided by the primary tumour is lost. In this model it cannot. It slows them. Three features of the model explain this result.

First, the satellites' angiogenic switch is not their first growth phase. Dermal micrometastases sit in well-perfused tissue and can grow to clinically detectable size by co-opting native vessels before they need new ones. Vessel co-option is a well-documented route by which tumours escape anti-angiogenic drugs [@kuczynski2019; @bergers2008]. In our simulations it made time to detection insensitive to every anti-VEGF regimen, even though neovascularisation was fully suppressed. The benefit appeared only in the later, angiogenesis-dependent phase. Here blockade capped lesion density and delayed major recurrence by roughly the length of treatment.

Second, dormancy is decided by the immune system. The linear condition @eq:dormancy contains no VEGF term. A micrometastasis is held dormant when effector density exceeds $m^{*}$, and anti-VEGF therapy can change this only indirectly. These indirect effects work in opposite directions. Removing VEGF relieves endothelial anergy, $\psi(v) \to 1$ [@motz2011; @gabrilovich1996; @huang2012]. Pruning neovessels lowers $b$ and therefore effector entry. Which effect wins depends on the phenotype. In phenotype B, relief of anergy dominated, and continuous therapy turned progressive disease into a controlled state. In phenotype A, and with strong immune recruitment, vessel loss dominated, and therapy was neutral or slightly harmful. The same trade-off caused the mild antagonism with sub-curative checkpoint blockade. It mirrors the "normalisation window" argument [@jain2005; @fukumura2018]: an anti-angiogenic dose that is too strong or lasts too long can reduce immune infiltration instead of improving it.

Third, the benefit lasts only while the drug is present. After a finite course, satellites that had kept growing on co-opted vessels revascularised within about 100–150 days of the last dose. In phenotype A, the system returned to the same long-term state as surgery alone. We found no VEGF overshoot after withdrawal, so the regrowth reflects resumption of a held-back process rather than the rebound reported in some preclinical settings [@ebos2009]. Our model does not include the hypoxia-driven selection of invasive clones described by Pàez-Ribes et al. [@paezribes2009], which could make the post-withdrawal phase worse.

These results agree qualitatively with AVAST-M, in which one year of adjuvant bevacizumab improved the disease-free interval without improving overall survival [@corrie2014; @corrie2018]. In the model, the same one-year schedule delays progression to major recurrence by about one year. It leaves time to detection almost unchanged, and long-term burden returns to the untreated level. The model suggests that a longer disease-free interval and an unchanged long-term outcome are both expected consequences of a treatment that pauses the angiogenic phase without changing the immune balance. Our phenotype analysis also suggests a hypothesis for biomarker work: patients whose tumours rely on VEGF-driven immune exclusion would benefit most, but only from long-term maintenance therapy.

The saturated dose–response has a practical implication. At the AVAST-M dose, tissue antibody exceeded $K_D$ by more than two orders of magnitude, so neutralisation was essentially complete. Reducing the dose by up to 90% hardly changed efficacy in either phenotype. If maintenance therapy were pursued, lower doses or longer dosing intervals could keep efficacy while reducing toxicity and cost. This prediction depends on our assumed tissue penetration and should be tested against tissue pharmacokinetic data. It is consistent with reports that lower, vessel-normalising doses can be as effective as high doses or more so [@huang2012].

Neoadjuvant therapy reduced the primary tumour but made its margin harder to judge. Because therapy lowered tumour density more than it shrank the footprint, a margin set from the visible edge left tumour behind more often. This led to earlier recurrence and to local persistence with narrow margins. The model represents this effect simply, but it points to a testable concern: margins planned after anti-angiogenic or other cytostatic pre-treatment may need to be set from pre-treatment imaging.

In the model, cure required strengthening the immune system soon after surgery. This happened when satellites were still small and systemic priming still high. A one-year checkpoint inhibitor started four weeks after excision cleared all satellites at moderate efficacy, whereas the same treatment started four months later did not. This matches the success of adjuvant checkpoint blockade after melanoma resection [@weber2017]. It suggests that anti-angiogenic therapy is better seen as a bridge than as a curative adjuvant. It could slow satellites that have already escaped while immune therapy takes effect, or serve as maintenance for VEGF-dependent, immune-excluded disease. Combined bevacizumab and ipilimumab increased immune infiltration in metastatic melanoma [@hodi2014]. Our results suggest that in the adjuvant setting, the timing and depth of vessel pruning need care, so that the combination does not reduce effector access to the satellites it is meant to clear.

The model also shows what pharmacodynamic markers can and cannot reveal. During therapy, total VEGF in tissue was higher than in untreated lesions of the same size, because antibody-bound VEGF is cleared more slowly than free VEGF, even though free VEGF fell by about 99%. A rise in measured total VEGF therefore indicates target engagement, not failure. Conversely, vessel density inside satellites stayed at the native level throughout treatment, even though the satellites kept growing. Imaging of perfusion or vessel density would thus show a "response" while the lesions were still expanding along co-opted vessels. In the model, the most informative markers of benefit were the ones linked to the immune compartment: effector recruitment and its recovery after surgery. This supports measuring immune infiltration in recurrent lesions alongside vascular markers in future studies of adjuvant anti-angiogenic therapy [@fukumura2018; @hodi2014].

### 4.1 Implications for trial design and testable predictions

The model makes several predictions that could be tested with existing data or simple experiments.

- **Endpoints.** In adjuvant anti-angiogenic trials, time to first detection and time to bulky or multifocal recurrence should respond differently. The model predicts little change in the first and a delay of roughly the treatment length in the second, followed by convergence after treatment stops. Reporting both endpoints, and the hazard over time rather than a single hazard ratio, would test this.
- **Duration.** If benefit fades after washout, extending treatment should prolong the delay roughly in proportion, while dose reduction should matter little. Pharmacokinetic data on tissue antibody levels after the last dose would show how quickly neutralisation is lost.
- **Patient selection.** The model expects the largest benefit in tumours where VEGF drives immune exclusion. These would show high VEGF expression together with low effector-cell infiltration and endothelial markers of anergy. Tumours with a strong existing immune infiltrate may gain nothing, or be slightly harmed by vessel pruning.
- **Co-option.** Satellites growing along existing dermal vessels should be insensitive to VEGF blockade at the time of detection. Histological assessment of co-option versus sprouting in recurrent satellites [@kuczynski2019] would test the mechanism behind this prediction.
- **Sequencing.** In animal models of resection with satellite seeding, giving immune checkpoint blockade early after surgery should matter more than adding anti-angiogenic therapy, and early blockade should be able to eliminate satellites that late blockade cannot.

These predictions do not depend on the exact parameter values. They follow from the structure of the model: immune-controlled dormancy, co-option-supported early growth, and reversible angiogenic dependence of established lesions.

### 4.2 Relation to previous models

Our baseline results without treatment reproduce the main finding of Eikenberry et al. [@eikenberry2009]: the immune response to a primary melanoma can suppress local metastases, and excision releases them. Our planar geometry replaces ring-shaped metastases with discrete satellites, and with this change the released satellites still exceeded the primary-tumour mass. We add a mechanistic description of an anti-VEGF antibody to this framework. The angiogenesis component simplifies the vascular-capacity concept of Hahnfeldt et al. [@hahnfeldt1999] and continuum angiogenesis models [@anderson1998] into a local, quasi-steady oxygen balance. The immune component follows the effector-limited killing of classical tumour–immune models [@kuznetsov1994; @depillis2005]. Our results add a spatial and pharmacological view to population-level models of post-surgical metastasis [@benzekry2016]. They also emphasise that a treatment can change the timing of recurrence without changing its long-term outcome. Analyses based only on disease-free endpoints may therefore overstate benefit.

### 4.3 Limitations

This is a conceptual, mechanistic model, and its predictions are qualitative.

- **Parameters.** Several immune, priming, co-option and drug-transport parameters are not directly measured. They were calibrated to reproduce the behaviour described above. The sensitivity analysis shows that the main conclusions hold over a ±50% range, but the size of each effect is uncertain.
- **Geometry.** The planar, depth-averaged geometry leaves out vertical invasion, the basement membrane, lymphatic spread and distant metastasis. In-transit disease spreads through lymphatics on scales of centimetres rather than millimetres.
- **Satellite seeding.** Seeding stops at surgery. Circulating tumour cells released afterwards, and seeding from satellites themselves, were not included.
- **Immune system.** The immune compartment is one lumped effector population. We did not represent regulatory cells, myeloid-derived suppressor cells, antigen-specific memory, or the exhaustion biology that checkpoint inhibitors act on. Checkpoint blockade was represented only as an increase in kill capacity.
- **Missing mechanisms.** We did not include wound healing after surgery and its inflammatory and angiogenic signals. We also did not include alternative angiogenic factors and the evolution of resistant or more invasive phenotypes [@bergers2008; @paezribes2009]. All three would probably reduce the benefit of anti-VEGF therapy further.
- **Recurrence thresholds.** Recurrence was defined by tumour-burden thresholds, which are only rough proxies for clinical detection.

## 5. Conclusions

A spatial model that couples surgery, satellite seeding, immune control, angiogenesis and anti-VEGF pharmacology predicts the following:

1. Excision releases dormant satellites from immune control, and they regrow to exceed the original tumour burden.
2. Adjuvant VEGF blockade does not delay detection of recurrence, because early satellite growth uses co-opted native vessels. It does delay major recurrence by about the length of treatment.
3. After a finite course, the benefit fades. Lasting control needs maintenance therapy and is largest in tumours with strong VEGF-mediated immunosuppression.
4. Clinical doses saturate VEGF neutralisation, so duration matters more than dose.
5. Neoadjuvant blockade can make edge-based margins unsafe.
6. Satellites can only be eliminated by strengthening the immune response early after surgery. Anti-VEGF therapy may support such treatment but does not replace it.

These predictions can be tested in experimental systems that combine resection of the primary tumour with longitudinal imaging of satellites, and in retrospective analyses that separate time to detection from time to major recurrence in adjuvant anti-angiogenic trials.

## Data and code availability

The C++ simulator, parameter files, experiment drivers, analysis scripts and figure-generation code needed to reproduce every result in this article are provided in the accompanying repository (folders model/ and tools/).

## Conflicts of interest

[To be completed by the authors.]

## Funding

[To be completed by the authors.]

## References

@@refs
