# pet_forecast: time-series forecasting of online petitions using Bayes
(for code description see bottom)


## Data & Exploratory Analysis
The data was gathered between July 2007 and April 2015 from the website \textit{epetitions.direct.gov.uk} using an automated script. Apart from a steep initial increase, the number of created petitions shows a steady growth rate in the observed time period. This site was maintained by the government until 30th March 2015 and subsequently replaced with a newer one (\textit{petition.parliament.uk}). In total, our data set includes 60,950 online petitions, of which 255 attracted more than 10,000 signatures and 41 more than 100,000 signatures. In total, 15\,201\,511 signatures were collected.

The time-series data contains signatures for all petitions at an hourly resolution. Additionally, we have the petition's main text, its author, the corresponding government department, opening date and closing date. As petitions are usually open for one year, we have approximately 365*24 = 9000 data points for each petition time-series. In the total signatures distribution plot below, we can confirm the distribution following a something similar to a power-law. We were able to verify the signatures curve changing shape at both the critical values of 10\,000 and 100\,000 signatures as in (Yasseri et al.) on a much larger dataset. However, the change at 100\,000 is far more drastic meaning that petitions rarely grow much larger after achieving this mark.

Data and motivation comes from research conducted at the Oxford Internet Institute, more specifically
[Yasseri et al.](https://arxiv.org/abs/1308.0239) and [Hale et al.](https://arxiv.org/abs/1304.0588). Note: I was able to access the data while doing this project and the figures are created from that time.


### Signatures 
The time-series data contains signatures for all petitions at an hourly resolution. Additionally, we have the petition's main text, its author, the corresponding government department, opening date and closing date. As petitions are usually open for one year, we have approximately 365 * 24  ~ 9000 data points for each petition time-series. In the figure below, we can confirm the distribution of signatures following a multi-scale power-law. We were able to verify the signatures curve changing shape at both the critical values of 10000 and 100000 signatures. However, the change at 100000 is far more drastic meaning that petitions rarely grow much larger after achieving this mark. This is because the goal of any online petition is to reach 100k, which will prompt a parliamentary debate.
<img src="https://user-images.githubusercontent.com/29401818/36397708-c4f9e80c-15bb-11e8-8d8c-bc35783410cb.png" height="400">

### Petition text
Before a petition is launched, there is no information about whether it is going to be successful or not. Moreover, as the shapes of the cumulative signature curves vary greatly, it is even harder to tell what the value will be at a certain time. To support our adaptive forecasting algorithm which will be introduced in Section 4, we aim to pre-classify the petitions based solely on a-priori information.
Specifically, we assume that most information about a petition can be extracted from its text description and that 'similar' petitions tend to follow similar curves during the observation period. Hence we categorise a petition based on its description text and subsequently utilise our prediction algorithm using parameters that were trained on petitions of this category.

More concretely, we structure our tokenized input text and use the bag-of-words model, where a text just corresponds to a collection of words. For simplicity, we only include unigrams (1-grams) and exclude higher order $n$-grams, which are terms containing $n$ words together in a certain order. Here, we assign each text description a vector of the words that have appeared. The rows of this sparse vector will correspond to the different words that occurred in all the descriptions. This vector is cleaned of common English stop words such as `the' or `and' and words common in any petition like `petition' or `signature'. Next, we utilise the \mbox{tf-idf} statistic on these high dimensional vectors. It is a frequently utilised weighting scheme in information retrieval


<img src="https://user-images.githubusercontent.com/29401818/36397065-e10ba42a-15b8-11e8-8625-cdbae0e7ce30.png" height="400">

<img src="https://user-images.githubusercontent.com/29401818/36397014-b1e25158-15b8-11e8-9da8-f3eb6ed3f0e1.png" height="400">

<img src="https://user-images.githubusercontent.com/29401818/36396996-9b33f9d4-15b8-11e8-868e-dff957a0eb18.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://user-images.githubusercontent.com/29401818/36396995-9b1a8efe-15b8-11e8-8799-fa1e8538398d.png" height="200">
<img src="https://user-images.githubusercontent.com/29401818/36396998-9b481cca-15b8-11e8-8e37-105478d94377.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://user-images.githubusercontent.com/29401818/36396999-9b626b48-15b8-11e8-96ac-87bbd6799ee4.png" height="200">

By using $K=4$ we can obtain three quite distinct clusters with silhouette scores above zero and are left with one cluster in the middle. However, the 'curse' of high-dimensional space \citep{Bellmann2003} results in very high overall distances (low silhouette scores) and the PCA projection may hide important features apparent in the topology of the data. Hence, we check the detected clusters by creating wordclouds (pictures of words that we scale according to their tf-idf score) of the centroid vectors.

From the wordcloud figures we can confirm clusters 0, 1 and 3 representing distinct topics. These are children/eduction, taxes/benefits and  Scottish/EU referendum, while cluster 2 seems to contain rather unspecific terms, as could be presumed from the PCA plot above.

## Example petition time-series
<img src="https://user-images.githubusercontent.com/29401818/36397047-d27a6c52-15b8-11e8-9a00-b57db4b35ce9.png" height="250">&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://user-images.githubusercontent.com/29401818/36397048-d2929ab6-15b8-11e8-8e51-1104d10f2465.png" height="250">


### Twitter Users

<img src="https://user-images.githubusercontent.com/29401818/36590428-8d92d464-1886-11e8-95f1-9ebc7740330e.png" height="200">

<img src="https://user-images.githubusercontent.com/29401818/36397016-b20f9db6-15b8-11e8-8394-b29935fa817a.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://user-images.githubusercontent.com/29401818/36397017-b2269b4c-15b8-11e8-8e2b-8f8409ace6ef.png" height="200">


## Model

## Results

<img src="https://user-images.githubusercontent.com/29401818/36590443-9bb472d2-1886-11e8-93b0-6b8c1b159e14.png" height="300">&nbsp;&nbsp;&nbsp;<img src="https://user-images.githubusercontent.com/29401818/36590444-9bc768ba-1886-11e8-999a-6aa86a36346e.png" height="300">


## Code
