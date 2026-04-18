# Bam-Dan Methodology Notes

This note is intended as an internal methodology reference for the `bam-dan` quiz. It should not be treated as a neutral academic truth claim, an official party classification, or a substitute for expert political science review.

Because Bangladeshi politics is sensitive, this document follows three rules:

1. It explains the scoring logic exactly as implemented in code.
2. It distinguishes between high-confidence placements and low-confidence placements.
3. Where the public record is too thin or too unstable, it says so and does not over-claim.

## 1. What The Quiz Measures

The quiz uses a two-axis model:

- Economic axis: left vs. right
- Social axis: secular/liberal vs. religious/conservative

The app does **not** claim that all Bangladeshi political life can be reduced to only two axes. It uses a two-axis model because it is understandable for users and operationally simple for a public quiz.

## 2. Which Questions Are Scored

Scored questions:

- Economic questions: `1, 2, 3, 4, 5, 6, 7, 8, 17, 18`
- Social questions: `9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22`

Unscored demographic questions:

- `101` Gender
- `102` Education
- `103` Occupation
- `104` Expatriate status
- `105` Age

Answer scale:

- `-2` = strongly disagree
- `-1` = disagree
- `0` = neutral
- `1` = agree
- `2` = strongly agree

## 3. How The Calculation Works

The server calculates the result by multiplying each answer by a question weight:

- Economic left-coded questions use weight `-1`
- Economic right-coded questions use weight `1`
- Social liberal/secular questions use weight `-1`
- Social conservative/religious questions use weight `1`

Then it sums the answers separately for the economic and social axes.

Normalization:

- `normalizedEconomic = (economicScore / (economicCount * 2)) * 10`
- `normalizedSocial = (socialScore / (socialCount * 2)) * 10`

That means each axis is normalized to roughly the range `-10` to `10`.

Current label thresholds in code:

- If `social > 4` and `economic > 0` → `Religious Right`
- If `social > 4` and `economic <= 0` → `Religious Left`
- If `economic < -3` and `social < 0` → `Leftist`
- If `economic > 3` and `social > 0` → `Rightwing`
- If `economic < 0` and `social < 0` → `Center Left`
- If `economic > 0` and `social > 0` → `Center Right`
- Otherwise → `Centrist`

Two implementation notes matter:

- The quiz has more social questions than economic questions, but normalization prevents the social axis from dominating purely because of question count.
- The result labels are threshold-based, not probabilistic. This is a heuristic classification, not a statistical latent-trait model.

### Known limitation: the Centrist bucket is unusually wide

The `Centrist` label is the catch-all for any respondent who does not meet any of the six named thresholds above. In practice this means a respondent with a strongly negative economic score (e.g. −8, firmly left) will still be classified as `Centrist` if their social score falls between `0` and `+4` — because the `Leftist` label requires *both* `economic < −3` *and* `social < 0`.

This is the direct mechanical cause of the "Centrist Illusion" finding: 52.4% of algorithm-classified Centrists have a negative economic score. They are not centrist economically — they are left-leaning on the economic axis but mildly conservative or neutral on the social axis, which places them outside all the named left categories and into the Centrist catch-all.

This is a known design trade-off, not a bug. The threshold logic was chosen for simplicity and user comprehension. Analysts working with this dataset should treat `Centrist` as a residual category, not a precise ideological classification.

## 4. Why These Questions Were Chosen

### Economic questions

These questions attempt to capture classic redistribution vs. market preference:

- Q1, Q3, Q5, Q7, Q17 represent state intervention, social welfare, labour protection, and environmental regulation.
- Q2, Q4, Q6, Q8, Q18 represent market openness, private initiative, foreign investment, property autonomy, and growth-first logic.

In plain terms, the economic axis asks whether the respondent prefers:

- stronger redistribution, labour rights, public services, and regulatory power, or
- stronger market freedom, investment openness, and private control.

### Social questions

These questions attempt to capture secular/plural/liberty-oriented views versus religious/traditional/order-oriented views:

- Q9, Q11, Q13, Q15, Q20, Q22 represent religiously informed law, traditional social authority, mandatory religion-based education, cultural protectionism, stronger speech restrictions for religious offense, and sameness-over-group-rights.
- Q10, Q12, Q14, Q16, Q19, Q21 represent equal citizenship, bodily autonomy and dress freedom, freedom of expression, equal inheritance/property rights for women, equal treatment of religious communities, and minority/indigenous protections.

This axis is not only about religion in the narrow sense. It also includes:

- pluralism
- freedom of expression
- women's autonomy
- minority rights
- indigenous rights

## 5. Why Women's Freedom And Empowerment Must Stay Central

Question `16` asks whether sons and daughters should have equal property rights. That is intentionally not a side issue. It is central.

Question `12` asks about personal freedom in dress and way of life. Question `14` asks about expression. Together, these questions speak to women's agency, bodily autonomy, and civic freedom.

This matters especially because women are roughly half of Bangladesh's population. The World Bank gender data portal reports Bangladesh's female population at about `50.83%` of total population for 2024, drawing on UN population estimates. A methodology that ignores women's rights would therefore ignore the interests of roughly half the country.

The quiz therefore treats women's equality not as a special-interest topic, but as a core indicator of where a respondent stands on the social axis.

## 6. Why Freedom Questions Matter

Some users may see free speech, dress freedom, minority protection, and indigenous rights as separate topics. In this quiz they are grouped together because, in practice, they all test whether the respondent prefers:

- a more liberty-protecting and plural order, or
- a more authority-protecting and norm-enforcing order.

That is why:

- freedom of expression (`Q14`)
- dress and lifestyle freedom (`Q12`)
- equal citizenship across religions (`Q19`)
- minority and indigenous accommodation (`Q21`)

all sit on the same broad social axis.

## 7. Known Limitations

- A two-axis model simplifies a much more complicated political reality.
- Bengali nationalism, Islamic politics, anti-authoritarian politics, class politics, and post-1971 memory do not fit perfectly into a single left-right scheme.
- The `Centrist` label is a residual catch-all category — see Section 3 for the specific threshold limitation.
- This quiz is educational and heuristic. It is not a substitute for survey research with validated scales.

## 8. Recommended Public Positioning

If this methodology is ever published, the safest wording is:

- this is an educational political-orientation quiz
- the result categories are heuristic, not definitive
- any political examples used are illustrative, not official endorsements or final scholarly judgments

That wording is especially important in Bangladesh's current political environment.

## 9. Sources Used For This Note

Code sources:

- `src/constants.ts`
- `server.ts`

External references:

- World Bank Gender Data Portal, female share of total population in Bangladesh:
  - https://genderdata.worldbank.org/en/indicator/sp-pop-totl-fe-zs
- SATP summary of Hefazat's 13-point demands:
  - https://www.satp.org/document/paper-acts-and-oridinances/13-point-demand
