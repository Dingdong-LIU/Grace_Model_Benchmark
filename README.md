# Grace_Model_Benchmark
A Banch Mark for LLM's performance in Grace Project. Using self-collected Cantonese Dataset.

## Speed Test

Below are the execution time of the three models on the test set. The execution time is measured in seconds.

![image](doc/execution_time_hist.svg)

![image](doc/execution_time_kde.svg)

<!-- SUMMARY_STATISTICS_PLACEHOLDER_BEGIN -->
|       |      GPT-4 |   GPT-4 Turbo |   GPT-4 Omni |
|:------|-----------:|--------------:|-------------:|
| count | 440        |    440        |   440        |
| mean  |   1.71998  |      1.31042  |     0.817352 |
| std   |   1.7527   |      0.768986 |     0.317143 |
| min   |   0.582766 |      0.617619 |     0.543163 |
| 25%   |   0.739138 |      0.851766 |     0.659441 |
| 50%   |   0.98635  |      1.03933  |     0.722345 |
| 75%   |   2.02726  |      1.41503  |     0.817539 |
| max   |  10.0983   |      5.39358  |     3.76859  |
<!-- SUMMARY_STATISTICS_PLACEHOLDER_END -->

## Accuracy Test

Below are the accuracy of the three models on the test set. The accuracy is measured using self-collected Cantonese dataset. Human evaluation is included to provide a reference.

<!-- SUMMARY_ACC_PLACEHOLDER_BEGIN -->
|       |      GPT-4 |   GPT-4 Turbo |   GPT-4 Omni |
|:------|-----------:|--------------:|-------------:|
| count | 440        |    440        |   440        |
| mean  |   0.965909 |      0.929545 |     0.943182 |
| std   |   0.181669 |      0.256203 |     0.231758 |
| min   |   0        |      0        |     0        |
| 25%   |   1        |      1        |     1        |
| 50%   |   1        |      1        |     1        |
| 75%   |   1        |      1        |     1        |
| max   |   1        |      1        |     1        |
<!-- SUMMARY_ACC_PLACEHOLDER_END -->

Note that:
* Compared with GPT-4, the other two model have better math calculation accuracy, especially for converting pounds to kilograms.
* However, the other two models have worse performance in filling additional information. For example, if a patient said "偶然多啲，通常都ok。" for sputum, they tends to believe it as "Unclear".