# AI_Nutrition_Analysis

An AI-powered food image analysis application that identifies food items from uploaded images and estimates their nutritional values using **Google Gemini, Retrieval-Augmented Generation (RAG), ChromaDB, and USDA FoodData Central**.

The application allows users to upload food images and view estimated calories, protein, carbohydrates, fat, and fiber in a simple, responsive web interface.

## Project Overview

AI Nutrition Analysis combines computer vision capabilities of a multimodal Large Language Model with nutrition information retrieved from an external food database.

Instead of manually entering food names and quantities, users upload an image of their meal. Gemini identifies the visible food items and estimates their edible quantities. ChromaDB helps map detected food names to suitable USDA search terms, and USDA FoodData Central provides the nutritional information used to calculate the combined meal values.

## Key Features

- **AI Food Identification:** Identifies multiple food items from uploaded food images using Google Gemini.
- **Portion Estimation:** Estimates the edible quantity of identified food items in grams.
- **RAG Integration:** Uses ChromaDB to retrieve relevant food-name mappings and improve USDA search queries.
- **USDA Nutrition Retrieval:** Retrieves nutritional information from USDA FoodData Central.
- **Combined Nutrition Calculation:** Aggregates the nutritional values of all detected food items into one meal-level result.
- **Multiple Image Upload:** Supports up to two food images per analysis.
- **Nutrition Dashboard:** Displays total calories, protein, carbohydrates, fat, and fiber.
- **Responsive Interface:** Provides a user-friendly interface for desktop and mobile devices.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Large Language Model | Google Gemini |
| RAG Framework | ChromaDB |
| Nutrition Database | USDA FoodData Central API |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Vercel |
| Environment Management | Python-dotenv |

## System Architecture

The application follows a simple pipeline architecture that connects image analysis, retrieval, nutrition data extraction, and result aggregation.

## Project Workflow


<img width="1323" height="1189" alt="image" src="https://github.com/user-attachments/assets/e14fc373-303f-4b6a-a0fe-269a765889ce" />


## How It Works

**1. Image Upload**

The user uploads one or two food images through the web interface. Images are validated and compressed before submission.

**2. Food Identification Using Gemini**

The Gemini model analyzes the uploaded images and identifies visible food items. It returns structured JSON containing food names and estimated edible quantities in grams.

**3. Food Mapping Using RAG and ChromaDB**

The detected food names are passed to the ChromaDB collection. The retrieval process finds relevant food-name mappings from the knowledge base and provides suitable search terms for USDA.

**4. Nutrition Retrieval Using USDA API**

The mapped food names are used to search USDA FoodData Central. The application retrieves available nutritional information, including:

- Energy (kcal)
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)

**5. Nutrition Calculation**

The retrieved nutritional values are calculated according to the estimated edible portion.

For each nutrient:

`Portion Value = (Nutrient per 100 g × Estimated Portion in g) / 100`

**6. Combined Nutrition Results**

The application aggregates the nutritional values of all identified food items and displays one combined meal-level result.

## Project Structure

```text
AI-Nutrition-Analysis/
│
├── app.py
├── gemini_service.py
├── rag.py
├── usda_api.py
│
├── requirements.txt
├── .python-version
├── .gitignore
├── vercel.json
├── README.md
│
├── knowledge/
│   └── food_aliases.txt
│
├── templates/
│   └── index.html
│
└── public/
    └── favicon.png
```

## Installation and Local Setup

**Prerequisites**

- Python 3.10 for local development
- Google Gemini API key
- USDA FoodData Central API key
- Git

**1. Clone the repository**

```bash
git clone https://github.com/VaibhavGovindwar/AI_Nutrition_Analysis.git
cd AI_Nutrition_Analysis
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```


**4. Run the application**

```bash
python app.py
```

Open the application in your browser:


## API Configuration

**Google Gemini API**

Used for food identification and edible portion estimation.

Get an API key from: https://aistudio.google.com/apikey

**USDA FoodData Central API**

Used to retrieve nutritional information for identified food items.

Get an API key from: https://fdc.nal.usda.gov/api-key-signup.html

## Vercel Deployment

The application is configured for deployment on Vercel.

1. Push the project to a GitHub repository.
2. Import the repository into Vercel.
3. Configure the required environment variables:
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL`
   - `USDA_API_KEY`
4. Deploy the application.
5. Test image uploads and nutrition analysis using the deployed URL.

The `.python-version` file specifies the Python runtime used for deployment.

## Limitations

- Food identification and portion estimation are AI-generated approximations.
- Actual food quantities and nutritional values may differ from the estimates.
- USDA database matches may not represent the exact recipe or preparation method.
- Nutrient availability depends on the selected USDA food record.
- The application supports a maximum of two uploaded images per analysis.
- The application requires internet connectivity to access Gemini and USDA APIs.

**Disclaimer:** This application is intended for informational and educational purposes. It does not provide medically verified nutritional measurements or replace professional dietary advice.

## Future Enhancements

- Improve food identification and portion estimation accuracy.
- Expand food-name mappings for regional Indian dishes.
- Improve matching of recipes and food preparation methods with nutrition database records.
- Add support for more food images and additional food categories.

## Author

**Vaibhav Govindwar**

M.Tech Data Science Student

Interested in Artificial Intelligence, Machine Learning, Deep Learning, and Data Science.

[GitHub](https://github.com/VaibhavGovindwar) · [LinkedIn](https://www.linkedin.com/in/vaibhav-govindwar)

---

*Built as an AI and RAG-based application combining multimodal food recognition with external nutritional data retrieval.*
