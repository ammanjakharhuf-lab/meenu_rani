@@title Mechanical Characterization and Performance Evaluation of Polymer–ZnO Composite Structures Manufactured by Additive Manufacturing

@@meta [Author names]

@@meta [Department, institution, city, country] · Corresponding author: [e-mail]

## Abstract

This chapter describes an experimental procedure for producing poly(lactic acid)–zinc oxide (PLA–ZnO) composite specimens by material-extrusion additive manufacturing and for evaluating them with three basic mechanical tests. Four compositions were prepared, containing 0, 1, 3 and 5 wt% ZnO. Dried ZnO powder was dispersed in anhydrous ethanol on a magnetic stirrer and coated onto dried PLA pellets. The ethanol was then evaporated, and the coated pellets were melt-compounded and extruded into 1.75 mm filament. Filament diameter and melt flow index were checked for every batch. Tensile bars (ASTM D638 Type I), flexural bars (ASTM D790) and hardness blocks were printed flat on a filament-fed printer with 100 % infill and an alternating ±45° raster. The same plate layout was used for every composition. After conditioning at 23 °C and 50 % relative humidity, the specimens were tested in uniaxial tension, three-point flexure and Shore D indentation hardness, and every fractured specimen was inspected visually. The chapter defines the specimen geometry, printing parameters, test conditions, data-reduction equations, specimen identification scheme and statistical comparison, so that any measured difference can be attributed to ZnO content rather than to processing or test set-up. It also explains how to read the tensile, flexural, hardness and melt-flow results together, including the effect of ZnO on PLA melt stability.

**Keywords:** PLA–ZnO composite; material extrusion; fused filament fabrication; filament extrusion; tensile test; three-point flexural test; Shore D hardness; melt flow index; print orientation.

## 1. Introduction

Material-extrusion additive manufacturing, often called fused filament fabrication (FFF), builds a part by depositing a melted polymer strand, or road, through a heated nozzle, one layer at a time. A printed part is therefore not a uniform solid. It is an assembly of fused roads whose bonding, packing and orientation depend on the printing conditions. Tensile strength, flexural response and surface hardness of a printed coupon reflect both the material and the way it was deposited.

Poly(lactic acid) (PLA) is the most widely printed thermoplastic. It is stiff, prints at moderate temperatures and is made from renewable feedstock. Zinc oxide (ZnO) is an inexpensive inorganic powder that is added to PLA for antibacterial activity, ultraviolet absorption and possible stiffening. Rigid ZnO particles can raise the elastic modulus when load is transferred across a well-bonded particle–polymer interface. The same particles can also lower strength and elongation, for three reasons. Poorly bonded or agglomerated particles act as stress concentrators. Filler can change how well adjacent roads fuse. ZnO can also catalyse chain scission of PLA at melt temperatures, which lowers molecular weight during compounding and printing. Adding ZnO therefore does not guarantee better mechanical performance, and the net effect has to be measured.

The experimental question addressed here is whether a change in ZnO content from 0 to 5 wt% produces a reproducible change in tensile, flexural and hardness properties when the PLA grade, mixing route, filament production, printing parameters, specimen geometry and test procedure are all held constant. Answering it requires a printed unfilled-PLA control that passes through exactly the same preparation steps as the filled compositions, including the ethanol treatment and both extrusion passes. Comparing filled printed specimens with data-sheet values for virgin PLA would mix the effect of ZnO with the effect of reprocessing.

The chapter is organised as follows. Section 2 describes the materials, mixture preparation, filament production, specimen printing, conditioning and test methods (Figure 1). Section 3 explains how the measured results are reduced, compared and interpreted. Section 4 covers quality control and reproducibility, Section 5 states the limitations of the approach, and Section 6 gives the conclusions.

!fig[workflow](figures/fig1_workflow.png) Experimental sequence used to prepare and test the PLA–ZnO compositions. Steps 1–4 prepare the mixture, steps 5–6 produce and check the filament, steps 7–8 produce and condition the specimens, and step 9 covers the mechanical tests.

## 2. Materials and Methods

### 2.1. Materials

The matrix was an extrusion-grade PLA supplied as pellets ([supplier, grade, lot number]). The filler was ZnO powder ([supplier, purity, nominal particle size, lot number]). Anhydrous ethanol (≥ 99.5 %) was used only as a carrier liquid for dispersing the ZnO and was fully removed before melt processing. No compatibiliser, plasticiser or surface treatment was used, so the compositions are two-component PLA–ZnO mixtures. The same PLA lot and ZnO lot were used for all four compositions.

PLA absorbs moisture, and residual water hydrolyses PLA chains during melt processing. The PLA pellets were therefore dried at 60 °C for 6 h, and the ZnO powder was dried at 110 °C for 2 h to remove adsorbed water. Dried materials were stored in sealed containers with desiccant and used within 24 h.

### 2.2. Composition design

The ZnO content of each mixture is expressed as a mass fraction of the dry ingredients, as defined in @eq:wt.

$$ w_{\mathrm{ZnO}} = \frac{m_{\mathrm{ZnO}}}{m_{\mathrm{ZnO}} + m_{\mathrm{PLA}}} \times 100 $$ {#eq:wt}

Here $m_{\mathrm{ZnO}}$ and $m_{\mathrm{PLA}}$ are the weighed masses of ZnO and PLA in grams, and $w_{\mathrm{ZnO}}$ is in wt%. Table 1 gives the ingredient masses for 100 g of mixture. Each composition was prepared at 500 g, five times the Table 1 quantities, which provides enough filament for the full specimen set, purge material and spares. All masses were weighed on an analytical balance with 0.01 g resolution, and the actual masses were entered on the batch record.

!table[comp] PLA–ZnO compositions and ingredient masses per 100 g of mixture.
| Composition ID | ZnO content (wt%) | ZnO (g) | PLA (g) | Role in the comparison |
| Z0 | 0 | 0.00 | 100.00 | Unfilled control, processed identically |
| Z1 | 1 | 1.00 | 99.00 | Low loading |
| Z3 | 3 | 3.00 | 97.00 | Intermediate loading |
| Z5 | 5 | 5.00 | 95.00 | High loading |
note: Batches of 500 g were prepared by multiplying each mass by five. The composition ID is the first element of every specimen identifier (Table 5).

### 2.3. Mixture preparation

Loose ZnO powder does not stay attached to dry PLA pellets. It segregates in the extruder hopper and produces filament with uneven filler content along its length. To avoid this, the ZnO was first dispersed in ethanol and then coated onto the pellets. The equipment used is shown in Figure 2.

For each filled composition, the weighed ZnO was added to anhydrous ethanol at about 10 mL of ethanol per gram of ZnO in a conical flask. The suspension was stirred on a magnetic stirrer (REMI 2MLH, Figure 2b) at 420 rpm for 30 min at room temperature (Figure 2d) to break up loose agglomerates. The dried PLA pellets were placed in a closed glass container, the suspension was poured over them, and the flask was rinsed into the container with a small volume of ethanol so that no ZnO was left behind. The container was rolled by hand at intervals while the ethanol evaporated in a fume hood, which left a uniform white coating of ZnO on the pellets. The coated pellets were then dried at 60 °C for 12 h to remove residual ethanol and moisture.

The unfilled control Z0 received the same treatment. Its pellets were wetted with the same volume of ethanol, without ZnO, and dried in the same way. Any effect of the ethanol treatment on PLA is therefore present in the control as well and cancels in the comparison. Each container was cleaned and dried between compositions. The batches were processed in order of increasing ZnO content (Z0, Z1, Z3, Z5) to limit carry-over of ZnO into lower-loaded batches.

!fig[equipment](figures/fig2_equipment.png) Laboratory equipment used for PLA–ZnO preparation, feedstock checks and printing: (a) Bambu Lab 3D printer with multi-spool filament feeder; (b) REMI 2MLH magnetic stirrer with flask, used to disperse ZnO in ethanol; (c) PACORR melt-flow-index tester, used to check every filament batch; (d) enlarged stirrer controller showing the 420 rpm stirring speed.

### 2.4. Filament production and feedstock checks

A single dry blending step does not distribute ZnO evenly through the PLA melt. Each batch was therefore extruded twice ([extruder make and model, screw diameter]). In the first pass, the coated pellets were melt-compounded, extruded as a strand, cooled in air and cut into pellets. In the second pass, these compounded pellets were extruded through a 1.75 mm die, drawn by a puller and wound onto a labelled spool. Both passes used the barrel temperature profile and screw speed given in Table 2, and all four compositions, including Z0, went through both passes. The first 100 g of extrudate from each pass was discarded to purge the previous material.

Filament diameter was measured with a digital micrometer at 20 points spaced 0.5 m apart, taking two perpendicular readings at each point to detect ovality. Filament was accepted when the mean diameter was 1.75 ± 0.05 mm and the ovality was below 0.05 mm. The mean diameter of each spool was entered into the slicer so that the extruded volume matched the intended road size.

Melt flow index (MFI) was measured on the PACORR tester (Figure 2c) at 210 °C under a 2.16 kg load, using chopped filament from each spool dried at 60 °C for 4 h. Five cut-offs were weighed per test, and the MFI was reported in g/10 min. MFI was measured because a rise in MFI relative to the processed Z0 control shows that the PLA molecular weight has fallen. Because ZnO can catalyse PLA chain scission, this check shows directly whether the filler has degraded the matrix during processing. The MFI results are interpreted together with the mechanical results in Section 3.4.

!table[process] Materials and feedstock-processing parameters.
| Step | Parameter | Setting |
| Drying of raw materials | PLA pellets | 60 °C, 6 h |
|  | ZnO powder | 110 °C, 2 h |
| ZnO dispersion | Carrier liquid | Anhydrous ethanol, about 10 mL per g ZnO |
|  | Stirring | Magnetic stirrer, 420 rpm, 30 min, room temperature |
| Pellet coating | Solvent removal | Evaporation in fume hood with periodic rolling |
|  | Drying | 60 °C, 12 h |
| Compounding pass | Barrel temperatures, feed to die | 170 / 180 / 190 / 190 °C |
|  | Screw speed | [rpm] |
|  | Output | Air-cooled strand, pelletised |
| Filament pass | Die diameter, target diameter | 1.75 mm; 1.75 ± 0.05 mm |
|  | Barrel temperatures, feed to die | 170 / 180 / 190 / 185 °C |
| Feedstock checks | Diameter | 20 points × 2 directions per spool |
|  | Melt flow index | 210 °C, 2.16 kg, five cut-offs per test |
| Storage | Before printing | Sealed bag with desiccant; filament dried 50 °C, 4 h before printing |
note: Values in square brackets depend on the extruder used and must be entered from the processing record.

### 2.5. Specimen design and 3D printing

Three specimen types were printed (Figure 3). Tensile specimens followed the ASTM D638 Type I geometry: overall length 165 mm, grip width 19 mm, narrow-section width 13 mm, narrow-section length 57 mm, fillet radius 76 mm and thickness 3.2 mm. Flexural specimens were rectangular bars 127 × 12.7 × 3.2 mm, which allows a support span of 51.2 mm at the 16:1 span-to-depth ratio of ASTM D790. Hardness specimens were blocks 40 × 40 × 6 mm. The 6 mm thickness meets the minimum thickness for Shore D readings, so the test surface does not need to be stacked.

!fig[specimens](figures/fig3_specimens.png) Specimen geometry. (a) ASTM D638 Type I tensile specimen with the 50 mm extensometer gauge length marked. (b) Flexural bar in top view and on the three-point supports. (c) Hardness block with the 12 mm edge margin and the five indentation sites.

Specimens were printed on the Bambu Lab printer (Figure 2a; [model]) fitted with a 0.4 mm hardened-steel nozzle. A hardened nozzle was used because ZnO is abrasive, and brass nozzle wear would gradually change the road width over the test series. Only one spool was loaded for each build. When a new composition was loaded in the multi-spool feeder, at least 50 g of the new filament was purged before the build started, so that no residue of the previous composition remained in the hot end.

The printing parameters are listed in Table 3. All specimens were printed flat on the plate (XY orientation) with 100 % rectilinear infill, two perimeters and a raster that alternated between +45° and −45° on successive layers (Figure 4b). With this orientation, the tensile load acts parallel to the layers (Figure 4c). The test therefore measures the in-plane response of the printed composite and does not load the interlayer bonds directly in tension. Each composition was printed as one plate containing five tensile specimens, five flexural bars and three hardness blocks, always in the same positions (Figure 4a). This layout keeps build-plate position effects the same for every composition.

!fig[build](figures/fig4_build_layout.png) Printing arrangement. (a) Plate layout used for every composition, with tensile (T), flexural (F) and hardness (H) specimens in fixed positions. (b) Alternating ±45° raster on successive layers. (c) Direction of tensile loading relative to the deposited layers in the flat (XY) build.

!table[print] Printing parameters, identical for all compositions.
| Parameter | Setting |
| Printer and nozzle | Bambu Lab [model]; 0.4 mm hardened-steel nozzle |
| Nozzle temperature | 210 °C |
| Bed temperature and surface | 60 °C; textured PEI plate, cleaned with isopropanol before each build |
| Layer height | 0.20 mm (first layer 0.20 mm) |
| Line width | 0.42 mm |
| Perimeters | 2 |
| Infill | 100 % rectilinear, alternating +45° / −45° |
| Print speed | 50 mm/s; first layer 20 mm/s |
| Part cooling fan | 100 % from layer 3 |
| Flow ratio | Calibrated once per spool and recorded |
| Build orientation | Flat (XY); tensile axis along X |
| Specimens per plate | 5 tensile, 5 flexural, 3 hardness (Figure 4a) |
| Environment | Enclosed printer; room temperature recorded for each build |

After printing, specimens were removed from the plate once the bed had cooled below 35 °C, to avoid bending them. Brims and loose strings were removed with a scalpel without touching the gauge section, the flexural span or the hardness test face. The specimens were not sanded.

### 2.6. Specimen identification, conditioning and pre-test inspection

Every specimen received an identifier of the form composition–build–type–position, for example Z3-B1-T4 for the fourth tensile specimen on the first build of the 3 wt% composition. The identifier was written on a grip end or edge with a fine marker and links each test result to the batch, spool and build records. The full test matrix is shown in Table 5.

Specimens were conditioned at 23 ± 2 °C and 50 ± 10 % relative humidity for at least 40 h before testing. The time between printing and testing was kept within the same range, between two and seven days, for all compositions, because PLA properties can change during storage through physical ageing.

Before testing, each specimen was inspected for warping, under-extrusion, gaps between roads, surface voids and stringing in the test region. The width and thickness were measured with a digital micrometer (0.001 mm resolution) at three points within the gauge section of tensile specimens and at mid-span and both support positions of flexural bars, and the mean values were used. Each specimen was weighed to 0.001 g. The apparent density was calculated with @eq:rho as a simple check on printing consistency.

$$ \rho_a = \frac{m}{V} $$ {#eq:rho}

Here $m$ is the specimen mass and $V$ is its volume, calculated from the measured dimensions. Flexural bars and hardness blocks have simple rectangular shapes and were used for this check. Within one composition, a bar whose apparent density differed by more than 2 % from the composition mean was flagged as a possible printing defect, and the flag was kept with its test result.

### 2.7. Uniaxial tensile testing

Tensile tests followed ASTM D638 on a universal testing machine ([make and model]) with a 5 kN load cell and wedge grips (Figure 5a). The specimen was centred in the grips with its long axis aligned with the load line. A clip-on extensometer with a 50 mm gauge length was attached to the narrow section. Tests ran at a constant crosshead speed of 5 mm/min until fracture. Force, crosshead displacement and extensometer extension were recorded at 10 Hz or faster.

!fig[setups](figures/fig5_test_setups.png) Test arrangements. (a) Uniaxial tension with wedge grips and a 50 mm clip-on extensometer. (b) Three-point flexure with 5 mm radius loading nose and supports at a 51.2 mm span. (c) Shore D durometer mounted on an operating stand with the block on a rigid flat support.

Engineering stress and strain were calculated from @eq:stress and @eq:strain.

$$ \sigma = \frac{F}{A_0} = \frac{F}{b\,h} $$ {#eq:stress}

$$ \varepsilon = \frac{\Delta L}{L_0} $$ {#eq:strain}

Here $F$ is the applied force, $A_0$ is the initial cross-sectional area of the narrow section, $b$ and $h$ are its measured width and thickness, $\Delta L$ is the extensometer extension and $L_0$ is the 50 mm gauge length. Crosshead displacement was not used for modulus, because grip seating and machine compliance add displacement that does not occur in the gauge section.

The tensile modulus $E$ was calculated as the least-squares slope of the stress–strain curve between 0.05 % and 0.25 % strain (@eq:mod; Figure 6a).

$$ E = \frac{\Delta \sigma}{\Delta \varepsilon}, \quad 0.0005 \le \varepsilon \le 0.0025 $$ {#eq:mod}

The maximum tensile stress $\sigma_{\max}$ is the peak force divided by $A_0$. The strain at maximum stress and the strain at break $\varepsilon_b$ were read from the extensometer record. If the extensometer had to be removed before fracture to protect it, the strain at break was calculated from crosshead displacement after a compliance correction, and this was noted on the result sheet.

### 2.8. Three-point flexural testing

Flexural tests followed ASTM D790 Procedure A on the same machine with a three-point fixture (Figure 5b). The loading nose and the two supports had a radius of 5 mm, and the support span $L$ was 51.2 mm, sixteen times the nominal thickness. Each bar was placed with its top printed face, the face last deposited, in compression and the bottom face, in contact with the plate during printing, in tension. Using this orientation for every specimen matters because the two faces differ in surface texture and road boundaries.

The crosshead rate $R$ was calculated from @eq:rate with a strain rate $Z$ of 0.01 mm/mm/min.

$$ R = \frac{Z L^{2}}{6 d} $$ {#eq:rate}

With $L$ = 51.2 mm and $d$ = 3.2 mm, $R$ is 1.37 mm/min. Each test ended at fracture of the outer surface or when the outer-fibre strain reached 5 %, whichever came first. Mid-span deflection was taken from the crosshead displacement corrected for fixture compliance, measured beforehand by loading the fixture against a rigid steel block.

The flexural stress, flexural strain and flexural modulus were calculated with @eq:flex, @eq:flexstrain and @eq:flexmod.

$$ \sigma_f = \frac{3 P L}{2 b d^{2}} $$ {#eq:flex}

$$ \varepsilon_f = \frac{6 D d}{L^{2}} $$ {#eq:flexstrain}

$$ E_B = \frac{L^{3} m}{4 b d^{3}} $$ {#eq:flexmod}

Here $P$ is the load, $D$ is the mid-span deflection, $b$ and $d$ are the measured width and thickness of the bar, and $m$ is the slope of the initial straight part of the load–deflection curve (Figure 6b). The flexural strength is $\sigma_f$ at the maximum load. If no break occurred before 5 % strain, the stress at 5 % strain was reported instead and labelled as such. These expressions assume small deflections and a rectangular cross-section, which hold for this geometry up to the 5 % limit.

### 2.9. Shore D indentation hardness

Hardness was measured with a Shore D durometer ([make and model]) mounted on an operating stand that applies a fixed 5 kg mass, which removes the variation caused by hand pressure (Figure 5c). Measurements followed ASTM D2240. Each block was placed on a rigid, flat support with the top printed face upward. Five readings were taken per block at the sites shown in Figure 3c. All sites were at least 12 mm from any edge and at least 6 mm from each other. The reading was taken 1 s after the presser foot made firm contact. With three blocks per composition, each composition has 15 readings. All readings were kept, not only the mean, so that differences between sites can be assessed. Readings that fell on a visible gap or seam were marked and repeated at an adjacent valid site.

### 2.10. Fracture inspection

Every tensile and flexural specimen was inspected after the test with the naked eye and a 10× hand lens, and was photographed beside a millimetre scale. For tensile specimens, the fracture location was coded as G (inside the extensometer gauge length), N (inside the narrow section but outside the gauge length), F (in the fillet) or J (at or inside the grip). Results with codes F and J were kept on the result sheet but excluded from the statistical comparison, because the stress at those locations is not the nominal gauge stress. The fracture surface was described as flat and brittle, stepped along roads, or showing visible necking or whitening. For flexural bars, the record noted whether the crack started on the tension face, whether it followed a road boundary and whether any layer separation appeared at the edge.

### 2.11. Test matrix and statistical analysis

Table 4 summarises the test conditions and Table 5 the test matrix. The tests were run in a rotating order (Z0, Z1, Z3, Z5, Z0, Z1 and so on) rather than finishing one composition before starting the next. Rotating the order spreads any drift in machine set-up or room conditions over all compositions.

!table[tests] Summary of mechanical test conditions and reported properties.
| Test | Standard and specimen | Key conditions | Reported properties |
| Uniaxial tension | ASTM D638 Type I, 3.2 mm thick | 5 kN load cell; 5 mm/min; 50 mm clip-on extensometer | $E$ (GPa), $\sigma_{\max}$ (MPa), strain at $\sigma_{\max}$ (%), $\varepsilon_b$ (%), fracture code |
| Three-point flexure | ASTM D790 Procedure A, 127 × 12.7 × 3.2 mm | Span 51.2 mm; nose and support radius 5 mm; 1.37 mm/min; bottom face in tension; stop at break or 5 % strain | $E_B$ (GPa), $\sigma_f$ (MPa), strain at $\sigma_f$ (%), failure description |
| Shore D hardness | ASTM D2240, 40 × 40 × 6 mm block | Operating stand, 5 kg; 1 s reading; five sites per block; rigid support | Individual readings, mean, standard deviation, range |
| Melt flow index | Chopped filament | 210 °C, 2.16 kg; five cut-offs | MFI (g/10 min) |

!table[matrix] Test matrix and number of specimens per composition.
| Composition | Tensile specimens | Flexural specimens | Hardness blocks (readings) | MFI tests | Example identifier |
| Z0 | 5 | 5 | 3 (15) | 3 | Z0-B1-T1 |
| Z1 | 5 | 5 | 3 (15) | 3 | Z1-B1-F2 |
| Z3 | 5 | 5 | 3 (15) | 3 | Z3-B1-H1 |
| Z5 | 5 | 5 | 3 (15) | 3 | Z5-B1-T5 |
| Total | 20 | 20 | 12 (60) | 12 | |

For each property, the results are reported as individual values and as the mean $\bar{x}$ and sample standard deviation $s$, together with the number of valid specimens $n$. The differences between the four compositions were tested by one-way analysis of variance (ANOVA). When the ANOVA was significant at $\alpha$ = 0.05, pairwise differences were identified with Tukey's honestly significant difference test. The change relative to the unfilled control was expressed with @eq:rel.

$$ \Delta X = \frac{\bar{X}_{\mathrm{Zi}} - \bar{X}_{\mathrm{Z0}}}{\bar{X}_{\mathrm{Z0}}} \times 100 $$ {#eq:rel}

Here $\bar{X}_{\mathrm{Zi}}$ is the mean of a property for composition Zi and $\bar{X}_{\mathrm{Z0}}$ is the mean for the processed unfilled control. A percentage change is described as an effect of ZnO only when the ANOVA and the pairwise test both show a significant difference.

!fig[reduction](figures/fig6_data_reduction.png) Data reduction. (a) Tensile stress–strain record, showing the strain interval used for the modulus, the maximum stress and the strain at break. (b) Flexural load–deflection record, showing the initial slope $m$, the maximum load and the 5 % strain limit. The curve shapes are illustrative and are not measured data.

## 3. Results Analysis and Discussion

### 3.1. Feedstock and specimen quality

The feedstock and specimen checks are examined before the mechanical results, because they decide whether the mechanical comparison is valid. The mean filament diameter and ovality of each spool, the MFI of each composition and the apparent density and defect flags of each specimen are tabulated against composition. If one composition shows lower apparent density, more defect flags or a wider diameter range than the others, its mechanical results reflect a printing problem as well as the filler. Such a composition is reprinted from new filament before it is compared.

### 3.2. Tensile response

Table 6 is the result table for the measured values. Tensile modulus, maximum stress and strain at break are compared across Z0, Z1, Z3 and Z5 using only the specimens that fractured inside the narrow section (codes G and N). Two typical patterns can be expected when a rigid particulate filler is added to a semi-crystalline polymer. The modulus may rise slightly with ZnO content, because the particles are much stiffer than PLA. The maximum stress and strain at break may fall, because particles and agglomerates start cracks and reduce the cross-section that carries load. A rise in modulus together with a fall in strength and elongation means the material has become stiffer and more brittle. It does not mean that the composite has been reinforced overall. The data in Table 6 decide which pattern applies.

!table[results] Measured properties of printed PLA–ZnO specimens (enter mean ± standard deviation, with the number of valid specimens n).
| Property | Z0 (0 wt%) | Z1 (1 wt%) | Z3 (3 wt%) | Z5 (5 wt%) | ANOVA p |
| Tensile modulus $E$ (GPa) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Maximum tensile stress $\sigma_{\max}$ (MPa) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Strain at break $\varepsilon_b$ (%) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Flexural modulus $E_B$ (GPa) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Flexural strength $\sigma_f$ (MPa) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Shore D hardness | [ ] | [ ] | [ ] | [ ] | [ ] |
| Melt flow index (g/10 min) | [ ] | [ ] | [ ] | [ ] | [ ] |
| Apparent density (g/cm³) | [ ] | [ ] | [ ] | [ ] | [ ] |
note: Tensile values include only specimens with fracture codes G and N. Report the individual specimen values in a supplementary table linked to the specimen identifiers.

Representative stress–strain curves, one per composition and chosen as the specimen closest to the group mean, are plotted on common axes. The curves show differences in ductility that summary numbers can hide. One example is a specimen that reaches a similar peak stress but breaks immediately afterwards instead of continuing to deform.

### 3.3. Flexural response and hardness

The flexural bar carries tension on one face and compression on the other, so its failure is controlled by the tension face. The flexural strength is usually higher than the tensile strength of the same material, because only a thin layer at the surface reaches the maximum stress. The ranking of the compositions can therefore differ between the two tests. A composition that loses tensile strength because of internal agglomerates may keep its flexural strength, since the maximum flexural stress acts only in the outermost roads. The flexural modulus is compared with the tensile modulus. Agreement between the two shows that the stiffness trend belongs to the material. If they disagree, the cause is often surface effects in the printed bar or compliance in the flexural fixture.

Shore D hardness measures resistance to local penetration of the surface. It responds mainly to the stiffness of the outermost material and to the surface texture of the printed roads. A small rise in hardness with ZnO is consistent with a stiffer surface, but it says nothing about load transfer through the specimen. If hardness rises while tensile strength falls, the two tests are measuring different aspects of behaviour, and they should be reported side by side rather than averaged into a single performance score. The spread of the 15 readings for each composition is reported along with the mean. A large spread between sites on the same block shows surface non-uniformity, which can be as informative as the difference between compositions.

### 3.4. Combined interpretation with melt flow index

The MFI result links processing to the mechanical response. If MFI rises steadily with ZnO content, the PLA molecular weight has fallen during compounding and printing. Shorter PLA chains reduce strength and elongation even when the filler is well dispersed. In that case, a fall in tensile strength with ZnO is at least partly caused by matrix degradation and not only by the particles themselves. If MFI stays close to the Z0 value while strength falls, degradation is not the main cause, and dispersion or bonding between roads is more likely. Including the processed Z0 control means that this comparison isolates the effect of ZnO from the effect of melt processing.

Fracture observations are read together with the force record. Table 7 lists common combinations of observations, their likely meaning and a simple follow-up test that can confirm it using the same methods described in Section 2.

!table[interpret] Interpretation of combined observations and follow-up checks.
| Observation | Likely meaning | Follow-up check with the same methods |
| Sudden load drop at low strain; flat fracture across roads | Brittle response; possible agglomerates or matrix degradation | Compare MFI with Z0; inspect fracture surface with the hand lens for white ZnO clusters |
| Fracture stepped along road boundaries | Weak fusion between adjacent roads | Check apparent density; reprint at 215 °C nozzle temperature and retest |
| Higher modulus but lower maximum stress and strain at break | Stiffening accompanied by earlier damage | Report all three properties; do not describe as reinforcement |
| Higher hardness but lower tensile strength | Surface stiffening without better bulk load transfer | Report hardness and tensile results separately |
| Large scatter within one composition | Uneven filler distribution or printing defects | Compare filament diameter records and defect flags; check results by plate position |
| Fracture in fillet or grip | Specimen or gripping problem, not a material result | Exclude from statistics; check grip alignment and fillet surface quality |

## 4. Quality Control and Reproducibility

Several controls in the procedure are aimed at reproducibility. Every composition used the same PLA and ZnO lots, the same ethanol treatment, the same two extrusion passes, the same printer, nozzle and slicer profile, the same plate layout and the same conditioning. Batch, spool, build and specimen records are linked through the specimen identifier, so any unexpected result can be traced back to its processing history.

The measuring instruments were checked before the test series. The load cell was verified with calibrated weights, the extensometer was checked against a calibration fixture, the micrometer was zeroed and checked against a gauge block, and the durometer was checked on its reference blocks. Grip alignment was checked with a straight steel bar, and the flexural support span was set with a vernier calliper and checked before each session.

Invalid tests were recorded with the reason, for example grip slippage, extensometer slip, fracture outside the narrow section or an indentation on a seam. They were excluded from the statistics but not deleted from the record. All five specimens printed for each test and composition were tested. No specimen was excluded only because its value seemed unusually high or low.

The procedure in this chapter characterises within-batch variation, because each composition was produced as one batch and printed as one plate. To show that the preparation route can be reproduced, a second independent batch of at least one composition, preferably Z3, can be prepared from fresh materials and tested in the same way. The difference between the two batch means can then be compared with the within-batch standard deviation.

## 5. Limitations

The procedure uses only basic tests: tension, three-point flexure, Shore D hardness, melt flow index and visual fracture inspection. It does not directly measure ZnO dispersion, particle size in the composite, crystallinity or molecular weight. Conclusions about mechanisms therefore remain inferences from the mechanical and MFI data, and they are stated as such. Microscopy of fracture surfaces, thermal analysis and filler-content measurement by ashing would confirm these inferences, but they lie outside the scope of this chapter.

All specimens were printed in one orientation (flat, XY) with a ±45° raster. The results describe the in-plane behaviour of this printed structure. They do not describe the through-thickness strength, which is controlled by interlayer bonding and is usually lower. A second orientation, with the tensile axis along Z, would need its own full set of compositions and should be compared within that orientation first.

The ZnO content is the nominal content of the weighed ingredients. Small losses of powder during coating and extrusion can make the actual content of the filament slightly lower than nominal, especially at 5 wt%. The ZnO content is therefore reported as nominal unless it has been measured.

## 6. Conclusions

This chapter has set out a complete experimental procedure for comparing 3D-printed PLA–ZnO composites containing 0, 1, 3 and 5 wt% ZnO. ZnO was dispersed in ethanol by magnetic stirring at 420 rpm and coated onto dried PLA pellets. The coated pellets were compounded and extruded into 1.75 mm filament, which was checked for diameter and melt flow index. Specimens were printed flat with 100 % infill and an alternating ±45° raster, using one fixed plate layout for every composition. Tensile, three-point flexural and Shore D hardness tests were run under defined standard conditions, followed by visual fracture inspection.

The design of the procedure separates the effect of ZnO from the effects of processing and test set-up. The unfilled control went through every preparation step, including the ethanol treatment and both extrusion passes. Specimen identifiers link each result to its batch, spool, build and plate position. Tests were run in rotating order, and differences were judged by ANOVA with pairwise comparison against the processed control. The melt flow index shows whether ZnO has degraded the PLA during processing, which helps to explain any loss of strength.

Tensile, flexural and hardness results measure different aspects of mechanical behaviour and are reported separately. A higher modulus or hardness with lower strength and elongation means a stiffer but more brittle material, not general reinforcement. The suitability of a given ZnO content should be judged against the property that matters most for the intended printed part, such as stiffness for a rigid spacer or strain at break for a clip or hinge.
