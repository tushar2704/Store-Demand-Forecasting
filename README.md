# Store Demand Forecasting



![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Canva](https://img.shields.io/badge/Canva-%2300C4CC.svg?style=for-the-badge&logo=Canva&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)
![Microsoft Office](https://img.shields.io/badge/Microsoft_Office-D83B01?style=for-the-badge&logo=microsoft-office&logoColor=white)
![Microsoft Word](https://img.shields.io/badge/Microsoft_Word-2B579A?style=for-the-badge&logo=microsoft-word&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Windows Terminal](https://img.shields.io/badge/Windows%20Terminal-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white)
## Problem Description

In the "Store Item Demand Forecasting" project, our goal is to predict the sales demand for various items in different stores based on historical sales data. The objective is to develop a machine learning model that can provide accurate forecasts for future sales of each store-item combination.
## Project Structure

The project repository is organized as follows:

```

├── LICENSE
├── README.md           <- README .
├── notebooks           <- Folder containing the final reports/results of this project.
│   │
│   └── store_demand.py   <- Final notebook for the project.
├── reports            <- Folder containing the final reports/results of this project.
│   │
│   └── Report.pdf     <- Final analysis report in PDF.
│   
├── src                <- Source for this project.
│   │
│   └── data           <- Datasets used and collected for this project.
|   └── model          <- Model.

```

## Dataset Information

The provided dataset contains historical sales records for different items across multiple stores. It is divided into two parts: the training dataset and the test dataset. The training dataset is utilized to train our predictive model and includes the following columns:

- `date`: The date of the sales record (in datetime format).
- `store`: The store ID where the item was sold.
- `item`: The item ID that was sold.
- `sales`: The quantity of items sold on the specific date, in the specific store, for the given item.

The test dataset mirrors these columns but lacks the sales information, which we need to predict.

## Background Information

Demand forecasting holds a pivotal role in supply chain management and retail operations. Accurate predictions of product demand enable businesses to optimize inventory levels, allocate resources effectively, and enhance overall operational efficiency. In the context of retail stores, precise demand forecasting is crucial to ensure the right product quantities are available at the correct time and location, thus preventing stockouts or overstocking.

Machine learning and time series forecasting techniques play a substantial role in addressing the challenges of demand forecasting. In this project, we will harness machine learning algorithms and time series analysis to construct a forecasting model capable of predicting future sales for different items in various stores.

The complexity arises from various factors that influence demand, including seasonality, trends, special events, and external elements like promotions or weather conditions. By comprehending and modeling these factors, our objective is to construct a resilient and accurate demand forecasting system.

## Objective

The primary objective of this project is to construct a machine learning model that can precisely predict future sales for different store-item combinations based on historical sales data. This will empower retailers to optimize inventory management, strategize promotions, and make data-driven decisions to effectively meet customer demand.

## Approach

To achieve our objective, we will follow these steps:

1. **Data Loading and Exploration**: We will load and explore the provided training and test datasets to grasp the data's structure and fundamental statistics.

2. **Feature Engineering**: Relevant time-related features will be extracted from the date column, and additional features will be created.

3. **Lag Feature Generation**: Lag features will be generated to capture past sales patterns, which are valuable for time series forecasting.

4. **Rolling Mean Features**: Rolling mean features will be applied to smoothen sales data and capture trends.

5. **Exponential Weighted Moving Averages (EWMA)**: EWMA will be employed to give more weight to recent sales data.

6. **Machine Learning Algorithms**: We will implement machine learning algorithms like LightGBM to train the model on historical sales data.

7. **Performance Evaluation**: The model's performance will be evaluated using metrics such as SMAPE (Symmetric Mean Absolute Percentage Error) to gauge the accuracy of our predictions.

8. **Prediction Generation**: Predictions will be made on the test dataset, generating sales forecasts for each store-item combination.

9. **Visualization and Comparison**: We will visualize the forecasted sales and compare them with actual sales to assess the effectiveness of the model.

By systematically following these steps, we aim to develop a robust machine learning model that can make accurate predictions about future sales, aiding retailers in making informed business decisions.
## License

This project is licensed under the [MIT License](LICENSE).
## Author
- <ins><b>©2023 Tushar Aggarwal. All rights reserved</b></ins>
- <b>[LinkedIn](https://www.linkedin.com/in/tusharaggarwalinseec/)</b>
- <b>[Medium](https://medium.com/@tushar_aggarwal)</b> 
- <b>[Tushar-Aggarwal.com](https://www.tushar-aggarwal.com/)</b>
- <b>[New Kaggle](https://www.kaggle.com/tagg27)</b> 

## Contact me!
If you have any questions, suggestions, or just want to say hello, you can reach out to us at [Tushar Aggarwal](mailto:info@tushar-aggarwal.com). We would love to hear from you!

