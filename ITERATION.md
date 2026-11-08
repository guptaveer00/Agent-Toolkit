# Iteration

## What went wrong

In the first central limit theorem review, the checker marked the large-sample normal approximation as supported by “PDF pages 89, 94.” The guide cited only PDF page 94 for that claim. The checker had found relevant material on page 89, but by counting it as support it answered a different question from whether the guide's own citation was sufficient. It also summarized the passages without identifying the exact result IDs.

## Diagnosis and change

Version 1 said to check the cited passage text and PDF page. It did not explain how to handle a relevant passage elsewhere in the same tool response. The output format also let the evidence field blur the distinction between a quotation and a conclusion drawn from the source.

I revised the skill to evaluate each claim using the pages cited for that claim. If an extra retrieved page supplies missing support, the checker now reports it separately as a citation gap. I also added a requirement to include the passage ID and a short exact excerpt, and to label any reasoning from the excerpt as a derivation.

## Rerun

I used the same drafts and MCP responses in new Codex sessions. On the central limit theorem guide, the revised checker supported the approximation using page 94 alone and identified the specific passage. It explicitly derived why quadrupling the sample size halves the standard deviation. On the confidence interval guide, it kept the coverage explanation supported and identified which of the two page 109 passages it relied on. That made it possible to trace each verdict back to the original MCP result.
