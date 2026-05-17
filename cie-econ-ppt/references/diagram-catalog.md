# Diagram catalog

Every diagram below is rendered by `scripts/diagrams.py`. To use one on a `diagram` slide, set `"diagram_id"` to the ID in the table. Don't invent IDs — if you need a diagram not on this list, fall back to a `content` slide and write a `## TODO: add diagram` line in the speaker notes so the user knows to add it.

You can override the diagram's built-in title with `"diagram_title": "..."` on the slide spec.

## Microeconomics

| diagram_id | What it shows | Typical use |
|---|---|---|
| `demand_supply` | D/S with equilibrium P*, Q* | Topic 2.1 baseline |
| `demand_supply_demand_right` | Rightward shift in D | Income rise, taste change |
| `demand_supply_demand_left` | Leftward shift in D | Substitute price falls |
| `demand_supply_supply_right` | Rightward shift in S | Tech improvement |
| `demand_supply_supply_left` | Leftward shift in S | Input cost rise, supply shock |
| `ppc` | Bowed-out PPC with A (efficient), B (inefficient), C (unattainable) | Topic 1.5 |
| `ppc_outward` | PPC shifts outward (growth) | Economic growth |
| `ppc_inward` | PPC shifts inward (recession / disaster) | Capital destruction |
| `elasticity_elastic` | Flat D | PED > 1 |
| `elasticity_inelastic` | Steep D | PED < 1 |
| `elasticity_unit` | Rectangular hyperbola | Unit elasticity |
| `elasticity_perfectly_elastic` | Horizontal D | Perfect competition firm demand |
| `elasticity_perfectly_inelastic` | Vertical D | Life-saving drugs |
| `surplus` | CS and PS shaded | Topic 2.5 |
| `indirect_tax` | S shifts up; tax incidence shaded | Topic 3.2 |
| `subsidy` | S shifts down; P_c < P* < P_p | Topic 3.2 |
| `price_ceiling` | Max price below P*; shortage | Topic 3.2 |
| `price_floor` | Min price above P*; surplus | Topic 3.2; min wage |
| `externality_neg_prod` | MSC > MPC; overproduction, welfare loss | Pollution |
| `externality_pos_prod` | MSC < MPC; underproduction | R&D spillover |
| `externality_neg_cons` | MSB < MPB; overconsumption | Smoking |
| `externality_pos_cons` | MSB > MPB; underconsumption | Vaccines, education |
| `indifference_budget` | IC + budget line + tangency optimum | Topic 7.2 (A2) |
| `cost_curves_sr` | MC, ATC, AVC, AFC | Topic 7.5 |
| `lrac` | U-shaped LRAC with MES | Topic 7.5 |
| `perfect_competition` | Firm with P=MC=AC at minimum | Topic 7.6 |
| `monopoly` | AR, MR, AC, MC; supernormal profit shaded | Topic 7.6 |
| `kinked_demand` | Two-slope D with MR gap | Topic 7.6 oligopoly |

## Macroeconomics

| diagram_id | What it shows | Typical use |
|---|---|---|
| `circular_flow` | Households ↔ Firms with injections & leakages | Topic 4.2 / 9.1 |
| `ad_as` | AD, SRAS, LRAS at long-run equilibrium | Topic 4.3 |
| `ad_as_ad_right` | Demand-pull stimulus | Topic 5.2, 5.3 |
| `ad_as_ad_left` | Contractionary policy / demand shock | |
| `ad_as_sras_right` | Positive supply-side / lower input costs | |
| `ad_as_sras_left` | Cost-push inflation | 1973 oil shock, 2022 |
| `phillips` | SRPC: trade-off between u and π | Topic 10.x |
| `laffer` | Tax revenue vs tax rate | Topic 5.2 |
| `lorenz` | Income inequality vs line of equality | Topic 3.3 / 8.2 |
| `money_market` | MD downward, MS vertical → r* | Topic 9.4 |

## International

| diagram_id | What it shows | Typical use |
|---|---|---|
| `tariff` | World price + tariff; q changes | Topic 6.2 |
| `exchange_rate` | D and S of currency → e* | Topic 6.4 / 11.2 |

## When to escalate

If a topic clearly needs a diagram absent from this list (e.g. monopolistic competition long-run, J-curve, price discrimination 1st/3rd degree, Big-Mac PPP, AD-AS with shifting LRAS), put a `content` slide in its place with a speaker note: `TODO_DIAGRAM: <description>`. The user will extend `scripts/diagrams.py` themselves.
