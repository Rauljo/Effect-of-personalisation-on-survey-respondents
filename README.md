# Effect-of-personalisation-on-survey-respondents

This experiment addresses the challenge of low response rates in online questionnaires by investigating
how message personalization and friendship closeness affect response rates and times. A randomized 2x2
factorial design was used, with 138 participants assigned to receive either a basic or a personalized message.
66 of these participants were close friends and 72 were not-so-close friends. The constraints due to the
skewness of the data resulted in a change of direction toward alternative methods other than ANOVA, such
as GLMs. The results showed that friendship closeness had a significant effect on the response rate, contrary
to message personalization. The high variance of the data made it impossible to distinguish any effects
of the factors in the response time. To obtain better results when examining message personalization and
friendship closeness, future studies should include larger sample sizes within a more homogeneous group of
participants, handle right-skewed data using alternative methods, and conduct the experiment under more
regulated conditions.

# Introduction

Online questionnaires have become increasingly prevalent due to their benefits, which include low cost,
scalability, and reduced transmission time. However, one of the drawbacks of these research instruments is
that they suffer from low response rates.
According to previous studies, modifying invitation or reminder messages may have an impact on questionnaire
response rates. For instance, personalizing salutations increase response rates by almost 40% compared
to an impersonal salutation (Joinson & Reips, 2007), while non-informative content can better attract
customer’s attention and increase the possibility that they will read and respond to an advertisement message
(Sahni et al., 2018).
This experiment aims to investigate whether the invitation message style influences online survey response
rates and response times among friends.

## This repository contains:
- Whattsapp bot: code to assign unique identifiers to contacts, assign types of messages randomly and send messages using a whattsapp bot
- Report: on the results on the analysis and possible future work
- Results: the dataset collected on the user inputs
- Data analysis code: All the histograms, plots, etc. used for the analysis (both in .qmd and .pdf formats)
