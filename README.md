# pet_forecast: time-series forecasting of online petitions using Bayes
(for code description see bottom)


## Data & Exploratory Analysis
The data was gathered between July 2007 and April 2015 from the website \textit{epetitions.direct.gov.uk} using an automated script. Apart from a steep initial increase, the number of created petitions shows a steady growth rate in the observed time period. This site was maintained by the government until 30th March 2015 and subsequently replaced with a newer one (\textit{petition.parliament.uk}). In total, our data set includes 60,950 online petitions, of which 255 attracted more than 10,000 signatures and 41 more than 100,000 signatures. In total, 15\,201\,511 signatures were collected.

The time-series data contains signatures for all petitions at an hourly resolution. Additionally, we have the petition's main text, its author, the corresponding government department, opening date and closing date. As petitions are usually open for one year, we have approximately 365*24 = 9000 data points for each petition time-series. In the total signatures distribution plot below, we can confirm the distribution following a something similar to a power-law. We were able to verify the signatures curve changing shape at both the critical values of 10\,000 and 100\,000 signatures as in (Yasseri et al.) on a much larger dataset. However, the change at 100\,000 is far more drastic meaning that petitions rarely grow much larger after achieving this mark.

Data and motivation comes from research conducted at the Oxford Internet Institute, more specifically
[Yasseri et al.](https://arxiv.org/abs/1308.0239) and [Hale et al.](https://arxiv.org/abs/1304.0588). Note: I was able to access the data while doing this project and the figures are created from that time.


### Signatures 
<img src="https://user-images.githubusercontent.com/29401818/36397708-c4f9e80c-15bb-11e8-8d8c-bc35783410cb.png" height="400">

### Users
<img src="https://user-images.githubusercontent.com/29401818/36397016-b20f9db6-15b8-11e8-8394-b29935fa817a.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp<img src="https://user-images.githubusercontent.com/29401818/36397017-b2269b4c-15b8-11e8-8e2b-8f8409ace6ef.png" height="200">


### Petition text
<img src="https://user-images.githubusercontent.com/29401818/36397065-e10ba42a-15b8-11e8-8625-cdbae0e7ce30.png" height="400">

<img src="https://user-images.githubusercontent.com/29401818/36397014-b1e25158-15b8-11e8-9da8-f3eb6ed3f0e1.png" height="400">

<img src="https://user-images.githubusercontent.com/29401818/36396996-9b33f9d4-15b8-11e8-868e-dff957a0eb18.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://user-images.githubusercontent.com/29401818/36396995-9b1a8efe-15b8-11e8-8799-fa1e8538398d.png" height="200">
<img src="https://user-images.githubusercontent.com/29401818/36396998-9b481cca-15b8-11e8-8e37-105478d94377.png" height="200">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://user-images.githubusercontent.com/29401818/36396999-9b626b48-15b8-11e8-96ac-87bbd6799ee4.png" height="200">

## Example petition time-series
<img src="https://user-images.githubusercontent.com/29401818/36397047-d27a6c52-15b8-11e8-9a00-b57db4b35ce9.png" height="250">&nbsp;&nbsp;&nbsp;&nbsp <img src="https://user-images.githubusercontent.com/29401818/36397048-d2929ab6-15b8-11e8-8e51-1104d10f2465.png" height="250">


## Model

## Results

<img src="" height="400">

<img src="" height="400">

<img src="" height="400">

<img src="" height="400">

<img src="" height="400">


## Code
