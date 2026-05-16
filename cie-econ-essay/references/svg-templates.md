# SVG Diagram Templates for CIE Economics

These are copy-pasteable SVG templates for the most common diagrams. Adapt the curve positions, labels, and shifts to the specific question. Embed them directly in the essay output — they render inline in any markdown viewer.

## How to use these

1. Pick the template closest to what the question needs.
2. Change labels (curve names, axis units, scenario-specific text) to match the question.
3. Adjust shift direction if needed (mirror the curve to shift the other way).
4. Place the SVG immediately after the prose that references it — and reference it in the prose ("As shown in Figure 1, supply shifts from S₁ to S₂…").

All templates use a 480×360 viewBox, with the plot area roughly 60–440 horizontally and 30–300 vertically. Origin at bottom-left of plot area.

## Conventions

- Axes: black, 2px, with arrowheads.
- Original curves: solid black, 2px.
- Shifted curves: solid blue (#1f77b4), 2px.
- Equilibrium points: small filled circles.
- Dashed projection lines to axes: stroke-dasharray="4,3", stroke="#888".
- Labels: font-family sans-serif, font-size 13–14px.
- Shaded areas (DWL, surplus, tax revenue): semi-transparent fill.

---

## 1. Demand and Supply — leftward supply shift

Use for: poor harvest, increased input costs, tax on producer, regulation reducing supply.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Demand and supply with leftward supply shift">
  <!-- Axes -->
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
  <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <!-- Axis labels -->
  <text x="455" y="305" font-size="13">Q</text>
  <text x="40" y="20" font-size="13">P</text>
  <!-- Demand: from (80, 60) to (430, 290) -->
  <line x1="80" y1="60" x2="430" y2="290" stroke="black" stroke-width="2"/>
  <text x="435" y="290" font-size="13">D</text>
  <!-- Original supply S1: from (80, 290) to (430, 60) -->
  <line x1="80" y1="290" x2="430" y2="60" stroke="black" stroke-width="2"/>
  <text x="435" y="60" font-size="13">S₁</text>
  <!-- Shifted supply S2: parallel, 80px to the left/up -->
  <line x1="160" y1="290" x2="430" y2="80" stroke="#1f77b4" stroke-width="2"/>
  <text x="170" y="285" font-size="13" fill="#1f77b4">S₂</text>
  <!-- Equilibrium E1 at intersection of D and S1: approximately (255, 175) -->
  <circle cx="255" cy="175" r="3.5" fill="black"/>
  <line x1="60" y1="175" x2="255" y2="175" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="255" y1="175" x2="255" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="42" y="179" font-size="12">P₁</text>
  <text x="248" y="316" font-size="12">Q₁</text>
  <!-- Equilibrium E2 at intersection of D and S2: approximately (295, 135) -->
  <circle cx="295" cy="135" r="3.5" fill="#1f77b4"/>
  <line x1="60" y1="135" x2="295" y2="135" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="295" y1="135" x2="295" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <!-- Wait: with leftward S shift, Q falls and P rises. Need to fix equilibrium positions. -->
</svg>
```

**Note on geometry:** if D is downward-sloping from (80,60) to (430,290), then at a given Q the price comes from D. When S shifts left (S₂ above/left of S₁), the intersection with D moves up-left → higher P, lower Q. The corrected positions:
- E₁ (S₁ ∩ D) ≈ (255, 175)
- E₂ (S₂ ∩ D) ≈ (215, 135) — higher up the D line (= higher P, lower Q)

Use these corrected coordinates:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Demand and supply with leftward supply shift">
  <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="455" y="305" font-size="13">Quantity</text>
  <text x="32" y="20" font-size="13">Price</text>
  <line x1="80" y1="60" x2="430" y2="290" stroke="black" stroke-width="2"/>
  <text x="435" y="290" font-size="13">D</text>
  <line x1="80" y1="290" x2="430" y2="60" stroke="black" stroke-width="2"/>
  <text x="435" y="60" font-size="13">S₁</text>
  <line x1="160" y1="290" x2="430" y2="80" stroke="#1f77b4" stroke-width="2"/>
  <text x="150" y="285" font-size="13" fill="#1f77b4">S₂</text>
  <circle cx="255" cy="175" r="3.5" fill="black"/>
  <line x1="60" y1="175" x2="255" y2="175" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="255" y1="175" x2="255" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="42" y="179" font-size="12">P₁</text>
  <text x="248" y="316" font-size="12">Q₁</text>
  <circle cx="215" cy="135" r="3.5" fill="#1f77b4"/>
  <line x1="60" y1="135" x2="215" y2="135" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="215" y1="135" x2="215" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="42" y="139" font-size="12" fill="#1f77b4">P₂</text>
  <text x="208" y="316" font-size="12" fill="#1f77b4">Q₂</text>
</svg>
```

**To shift demand instead (e.g. rise in income, normal good):** swap which line shifts. To shift right rather than left: mirror the second curve to the other side of the original.

---

## 2. AD-AS with rightward AD shift (Keynesian LRAS)

Use for: expansionary fiscal/monetary policy, increase in consumer confidence.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="AD-AS Keynesian, AD shifts right">
  <defs><marker id="arrow2" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="395" y="318" font-size="13">Real GDP (Y)</text>
  <text x="68" y="20" font-size="13">Price Level (PL)</text>
  <!-- Keynesian LRAS: horizontal then vertical at Yfe (x=370) -->
  <path d="M60 250 L370 250 L370 30" stroke="black" stroke-width="2" fill="none"/>
  <text x="375" y="40" font-size="13">LRAS</text>
  <!-- SRAS: upward sloping -->
  <line x1="80" y1="285" x2="430" y2="80" stroke="black" stroke-width="2"/>
  <text x="435" y="80" font-size="13">SRAS</text>
  <!-- AD1 -->
  <line x1="100" y1="60" x2="380" y2="290" stroke="black" stroke-width="2"/>
  <text x="92" y="56" font-size="13">AD₁</text>
  <!-- AD2 shifted right by ~80px -->
  <line x1="180" y1="60" x2="460" y2="290" stroke="#1f77b4" stroke-width="2"/>
  <text x="172" y="56" font-size="13" fill="#1f77b4">AD₂</text>
  <!-- E1: AD1 ∩ SRAS ≈ (220, 215) -->
  <circle cx="220" cy="215" r="3.5" fill="black"/>
  <line x1="60" y1="215" x2="220" y2="215" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="220" y1="215" x2="220" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="38" y="219" font-size="12">PL₁</text>
  <text x="210" y="316" font-size="12">Y₁</text>
  <!-- E2: AD2 ∩ SRAS ≈ (290, 175) -->
  <circle cx="290" cy="175" r="3.5" fill="#1f77b4"/>
  <line x1="60" y1="175" x2="290" y2="175" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="290" y1="175" x2="290" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="38" y="179" font-size="12" fill="#1f77b4">PL₂</text>
  <text x="280" y="316" font-size="12" fill="#1f77b4">Y₂</text>
  <!-- Yfe marker -->
  <line x1="370" y1="295" x2="370" y2="305" stroke="black" stroke-width="2"/>
  <text x="355" y="316" font-size="12">Yfe</text>
</svg>
```

**For Classical (vertical LRAS at Yfe) only:** replace the LRAS path with a single vertical line at x=370 from y=30 to y=300. AD shifts in the long run change PL only, not Y.

---

## 3. Negative externality of consumption (with welfare loss)

Use for: cigarettes, alcohol, sugary drinks, fast food, fossil fuel consumption.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Negative externality of consumption">
  <defs><marker id="arrow3" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="425" y="318" font-size="13">Quantity</text>
  <text x="22" y="20" font-size="13">Costs/Benefits</text>
  <!-- MPC = MSC (upward) -->
  <line x1="80" y1="290" x2="430" y2="60" stroke="black" stroke-width="2"/>
  <text x="430" y="55" font-size="13">MPC = MSC</text>
  <!-- MPB (downward) -->
  <line x1="80" y1="80" x2="430" y2="290" stroke="black" stroke-width="2"/>
  <text x="435" y="290" font-size="13">MPB</text>
  <!-- MSB (parallel, below MPB) -->
  <line x1="80" y1="140" x2="380" y2="290" stroke="#1f77b4" stroke-width="2"/>
  <text x="385" y="290" font-size="13" fill="#1f77b4">MSB</text>
  <!-- Free market eq Q1 (MPC ∩ MPB) ≈ (260, 180) -->
  <circle cx="260" cy="180" r="3.5" fill="black"/>
  <line x1="260" y1="180" x2="260" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="252" y="316" font-size="12">Q₁</text>
  <!-- Social optimum Q* (MSC ∩ MSB) ≈ (210, 195) -->
  <circle cx="210" cy="195" r="3.5" fill="#1f77b4"/>
  <line x1="210" y1="195" x2="210" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="200" y="316" font-size="12" fill="#1f77b4">Q*</text>
  <!-- Welfare loss triangle: between MSB and MPC from Q* to Q1 -->
  <polygon points="210,195 260,180 235,165" fill="#d62728" fill-opacity="0.35" stroke="#d62728" stroke-width="1"/>
  <text x="270" y="160" font-size="12" fill="#d62728">Welfare loss</text>
</svg>
```

The welfare-loss triangle vertices are: the social optimum point (Q*, MSC=MSB), the free-market point (Q₁, MPC=MPB), and the point above Q₁ where MSB meets the vertical at Q₁. Adjust the third vertex coordinates if you change Q₁.

---

## 4. Tariff diagram

Use for: import tariff, protectionism essays.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Tariff on imports">
  <defs><marker id="arrow4" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="425" y="318" font-size="13">Quantity</text>
  <text x="42" y="20" font-size="13">Price</text>
  <!-- Domestic demand Dd -->
  <line x1="80" y1="60" x2="430" y2="290" stroke="black" stroke-width="2"/>
  <text x="435" y="290" font-size="13">Dd</text>
  <!-- Domestic supply Sd -->
  <line x1="80" y1="290" x2="430" y2="60" stroke="black" stroke-width="2"/>
  <text x="435" y="60" font-size="13">Sd</text>
  <!-- World price Pw (horizontal at y=230) -->
  <line x1="60" y1="230" x2="445" y2="230" stroke="black" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="40" y="234" font-size="12">Pw</text>
  <!-- Pw + tariff at y=180 -->
  <line x1="60" y1="180" x2="445" y2="180" stroke="#1f77b4" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="22" y="184" font-size="12" fill="#1f77b4">Pw+t</text>
  <!-- Key Q points: -->
  <!-- Q1: Sd at Pw → solve. Sd from (80,290) to (430,60). At y=230, x = 80 + (290-230)/(290-60)*350 = 80 + 60/230*350 ≈ 80+91 = 171 -->
  <!-- Q2: Sd at Pw+t (y=180) → x = 80 + (290-180)/230*350 = 80 + 110/230*350 ≈ 80+167 = 247 -->
  <!-- Q3: Dd at Pw+t (y=180) → Dd from (80,60) to (430,290). At y=180, x = 80 + (180-60)/230*350 = 80 + 182 = 262 ... wait Dd is going down to the right meaning higher Q at lower P. At y=180 (higher P than Pw means lower Q on Dd): x = 80 + (180-60)/(290-60)*350 = 80 + 120/230*350 ≈ 80+182 = 262 -->
  <!-- Q4: Dd at Pw → x = 80 + (230-60)/230*350 = 80 + 259 = 339 -->
  <line x1="171" y1="230" x2="171" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="163" y="316" font-size="11">Q₁</text>
  <line x1="247" y1="180" x2="247" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="239" y="316" font-size="11">Q₂</text>
  <line x1="262" y1="180" x2="262" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="264" y="316" font-size="11">Q₃</text>
  <line x1="339" y1="230" x2="339" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="331" y="316" font-size="11">Q₄</text>
  <!-- Areas: a (producer gain), b (DWL), c (gov revenue), d (DWL) -->
  <polygon points="171,230 247,180 171,180" fill="#2ca02c" fill-opacity="0.25"/>
  <text x="195" y="208" font-size="11" fill="#2ca02c">a</text>
  <polygon points="247,180 171,230 247,230" fill="#d62728" fill-opacity="0.3"/>
  <text x="217" y="222" font-size="11" fill="#d62728">b</text>
  <polygon points="247,180 262,180 262,230 247,230" fill="#ff7f0e" fill-opacity="0.3"/>
  <text x="252" y="208" font-size="11" fill="#ff7f0e">c</text>
  <polygon points="262,180 339,230 262,230" fill="#d62728" fill-opacity="0.3"/>
  <text x="287" y="222" font-size="11" fill="#d62728">d</text>
  <!-- Legend -->
  <text x="320" y="40" font-size="11" fill="#2ca02c">a = producer gain</text>
  <text x="320" y="55" font-size="11" fill="#ff7f0e">c = govt revenue</text>
  <text x="320" y="70" font-size="11" fill="#d62728">b + d = DWL</text>
</svg>
```

---

## 5. Monopoly

Use for: monopoly questions, market power, allocative inefficiency.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Monopoly equilibrium">
  <defs><marker id="arrow5" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow5)"/>
  <text x="425" y="318" font-size="13">Quantity</text>
  <text x="38" y="20" font-size="13">Price/Cost</text>
  <!-- AR=D (downward) -->
  <line x1="80" y1="50" x2="430" y2="290" stroke="black" stroke-width="2"/>
  <text x="435" y="290" font-size="13">AR=D</text>
  <!-- MR (steeper, half slope) -->
  <line x1="80" y1="50" x2="255" y2="290" stroke="black" stroke-width="2"/>
  <text x="260" y="290" font-size="13">MR</text>
  <!-- AC (U-shaped, simplified as curve) -->
  <path d="M100 220 Q 220 180, 350 230" stroke="black" stroke-width="2" fill="none"/>
  <text x="355" y="232" font-size="13">AC</text>
  <!-- MC (upward, crosses AC at its minimum) -->
  <path d="M100 270 Q 200 200, 380 80" stroke="black" stroke-width="2" fill="none"/>
  <text x="385" y="80" font-size="13">MC</text>
  <!-- Qm where MC = MR: approximately (180, 180) on MR -->
  <circle cx="180" cy="180" r="3.5" fill="black"/>
  <line x1="180" y1="180" x2="180" y2="300" stroke="#888" stroke-dasharray="4,3"/>
  <text x="173" y="316" font-size="12">Qm</text>
  <!-- Pm: read off D at Qm -->
  <line x1="180" y1="118" x2="60" y2="118" stroke="#888" stroke-dasharray="4,3"/>
  <line x1="180" y1="180" x2="180" y2="118" stroke="#888" stroke-dasharray="4,3"/>
  <circle cx="180" cy="118" r="3.5" fill="black"/>
  <text x="38" y="122" font-size="12">Pm</text>
  <!-- AC at Qm: read off AC curve, approximately y=200 -->
  <line x1="180" y1="200" x2="60" y2="200" stroke="#888" stroke-dasharray="4,3"/>
  <text x="30" y="204" font-size="12">AC(Qm)</text>
  <!-- Supernormal profit rectangle -->
  <rect x="60" y="118" width="120" height="82" fill="#2ca02c" fill-opacity="0.18"/>
  <text x="95" y="165" font-size="11" fill="#2ca02c">Supernormal profit</text>
</svg>
```

---

## 6. Production Possibility Curve (PPC) with outward shift

Use for: economic growth, productivity, technological progress.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="PPC with outward shift">
  <defs><marker id="arrow6" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow6)"/>
  <text x="340" y="318" font-size="13">Consumer goods</text>
  <text x="68" y="20" font-size="13">Capital goods</text>
  <!-- PPC1: concave outward from (60, 80) to (320, 300) -->
  <path d="M60 80 Q 130 100, 320 300" stroke="black" stroke-width="2" fill="none"/>
  <text x="324" y="295" font-size="13">PPC₁</text>
  <!-- PPC2: outward shifted -->
  <path d="M60 40 Q 180 60, 410 300" stroke="#1f77b4" stroke-width="2" fill="none"/>
  <text x="414" y="295" font-size="13" fill="#1f77b4">PPC₂</text>
</svg>
```

---

## 7. Lorenz curve

Use for: income inequality questions.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="Lorenz curve">
  <defs><marker id="arrow7" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="black"/></marker></defs>
  <line x1="60" y1="300" x2="450" y2="300" stroke="black" stroke-width="2" marker-end="url(#arrow7)"/>
  <line x1="60" y1="300" x2="60" y2="20" stroke="black" stroke-width="2" marker-end="url(#arrow7)"/>
  <text x="310" y="318" font-size="13">Cumulative % population</text>
  <text x="70" y="20" font-size="13">Cumulative % income</text>
  <!-- 45-degree line of equality -->
  <line x1="60" y1="300" x2="360" y2="40" stroke="black" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="365" y="40" font-size="13">Line of equality</text>
  <!-- Lorenz curve: bowed below -->
  <path d="M60 300 Q 230 290, 360 40" stroke="#1f77b4" stroke-width="2" fill="none"/>
  <text x="200" y="270" font-size="13" fill="#1f77b4">Lorenz curve</text>
</svg>
```

---

## Adapting templates

- **Re-labelling:** change axis labels and curve names to match the question (e.g. "Quantity of coffee" rather than "Quantity"; "S (world supply)" rather than "S₁").
- **Re-colouring shifts:** the templates use blue (#1f77b4) for shifted curves. To show two consecutive shifts, use blue and then orange (#ff7f0e).
- **Mirroring:** to shift right instead of left (or up instead of down), swap the x-coordinates of the shifted curve's endpoints.
- **Adding shaded areas:** use `<polygon points="x1,y1 x2,y2 x3,y3" fill="#colour" fill-opacity="0.3"/>` and pick vertices from the intersection points.
- **Adding annotations:** small `<text>` elements at the right location, font-size 11–12px.

## When to use which

| Question topic | Template |
|---|---|
| Supply or demand shock in any market | #1 |
| Fiscal / monetary policy effects | #2 |
| Consumption externalities (demerit goods) | #3 |
| Tariffs, protectionism | #4 |
| Monopoly, market power | #5 |
| Economic growth, opportunity cost | #6 |
| Income inequality | #7 |

For diagrams not covered (PED, Phillips curve, exchange rate, kinked demand, etc.), adapt the closest template or fall back to the bracketed `[Diagram: …]` description format used in the main SKILL.md.
