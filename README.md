# ConCur : Application for Currency Conversion

## Project description

This web application hosts three tools for querying and visualizing data from a currency-based API, as well as operating currency conversion on a collection of almost 30 different currencies.

## Application URL

The application has been deployed using the Streamlit Community Cloud, and is available at [this URL]([https://www.data.gouv.fr](https://datacamp2024-iaxrg6qhvr39fgiksvpq4c.streamlit.app/) 

## How to use

### Login

You will first be met with a login page. The user can create a profile for themself if they wish, but can also use the pre-existing credentials below in order to log into the website.

#### -- Credentials
- (`Username : Romain`)
- (`Password : abc123`)

Double-click the login button to enter the website.

### Currency info

The first and only available select box at first will be the "Currency info". With this box, you can select an abbreviation corresponding to a currency, and visualize its full name & symbol.  
You can query informations regarding the currency with the first button, then confirm your choice with the second.

### Currency conversion

Once you confirm your choice, you will be brought to the proper currency converter, with the initial currency of the first field matching the one you chose.  
You can then choose the target currency with the second field, and use the third one to precise the amount to convert. The + and - buttons increment and decrement by 1.00.

### Historical trade exchange rate

After converting the chosen amount, you gain access to the third field. Using the select boxes, you can select an interval to visualize the historical trade exchange rate evolution
between the initial currency and the target currency chosen before.  

Note that the user can change the values of the initial and target currency at any point in the process, using the currency conversion
select boxes.

## Warnings (to read before usage) :

```diff
Due to the nature of the API, the queries are limited to 10 per minute. As such, it is unadvised to perform predicions on a large scale for the historical data section. It is advised that the user limit
their predicions to the past week.

Likewise, older historical is not available from the API. As such, it is also recommended that the user does not try to send queries for historical data anterior to 2024.
```

## Credits
General architecture & API requests : **Marwan Ben Selma**  
Database & Front End : **Romain Ferigo**  
Machine Learning implementation : **Kader Coulibaly***
