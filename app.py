from flask import Flask, request, render_template_string, redirect, session
import os
import datetime

app = Flask(__name__)
app.secret_key = 'sports-cars-secret-key-2024'

# Authentication
LOGIN_CREDENTIALS = {'username': 'admin', 'password': 'password'}

# Comprehensive Car Database
CAR_DATABASE = {
    # BMW Models
    "bmw m5": {
        "name": "BMW M5 Competition", "company": "BMW", "country": "🇩🇪 Germany",
        "year": "1984", "topspeed": "305 km/h", "engine": "4.4L V8 Twin-Turbo",
        "horsepower": "617 HP", "price": "$105,000", "type": "Sports Sedan",
        "info": "Ultimate driving machine with racetrack performance",
        "image": "https://images.pexels.com/photos/30166138/pexels-photo-30166138.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "bmw i8": {
        "name": "BMW i8", "company": "BMW", "country": "🇩🇪 Germany",
        "year": "2014", "topspeed": "250 km/h", "engine": "Hybrid Electric",
        "horsepower": "369 HP", "price": "$148,000", "type": "Sports Car",
        "info": "Futuristic hybrid sports car with butterfly doors",
        "image": "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iDKbTZKuItWE/v1/1200x-1.jpg"
    },
    
    # Tesla Models
    "tesla model s": {
        "name": "Tesla Model S Plaid", "company": "Tesla", "country": "🇺🇸 USA",
        "year": "2012", "topspeed": "322 km/h", "engine": "Electric Tri-Motor",
        "horsepower": "1,020 HP", "price": "$89,990", "type": "Electric Sedan",
        "info": "Fastest production car with autopilot technology",
        "image": "https://cdn.pixabay.com/photo/2021/01/15/16/49/tesla-5919764_1280.jpg"
    },
    "tesla roadster": {
        "name": "Tesla Roadster", "company": "Tesla", "country": "🇺🇸 USA",
        "year": "2023", "topspeed": "400+ km/h", "engine": "Electric",
        "horsepower": "1,400 HP", "price": "$200,000", "type": "Electric Sports",
        "info": "Fastest car in the world with SpaceX package",
        "image": "https://cdn.pixabay.com/photo/2020/11/22/18/55/cybertruck-5768187_1280.jpg"
    },
    
    # Tata Models
    "tata nexon": {
        "name": "Tata Nexon EV", "company": "Tata Motors", "country": "🇮🇳 India",
        "year": "2014", "topspeed": "180 km/h", "engine": "Electric",
        "horsepower": "143 HP", "price": "$18,000", "type": "Electric SUV",
        "info": "India's bestselling EV with 5-star safety rating",
        "image": "https://images.autox.com/uploads/2023/09/Tata-Nexon-Right-Front-Three-Quarter.jpg"
    },
    
    # Mahindra Models
    "mahindra thar": {
        "name": "Mahindra Thar", "company": "Mahindra", "country": "🇮🇳 India",
        "year": "2010", "topspeed": "155 km/h", "engine": "2.0L Turbo Petrol",
        "horsepower": "150 HP", "price": "$16,000", "type": "Off-roader",
        "info": "Iconic Indian off-roader with convertible top",
        "image": "https://images.pexels.com/photos/33101188/pexels-photo-33101188.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    
    # Mercedes Models
    "mercedes amg gt": {
        "name": "Mercedes-AMG GT", "company": "Mercedes", "country": "🇩🇪 Germany",
        "year": "2014", "topspeed": "318 km/h", "engine": "4.0L V8 Biturbo",
        "horsepower": "523 HP", "price": "$115,000", "type": "Sports Car",
        "info": "Handcrafted AMG performance with luxury interior",
        "image": "https://cdn.pixabay.com/photo/2017/03/27/14/56/auto-2179220_1280.jpg"
    },
    
    # Ford Models
    "ford mustang gt": {
        "name": "Ford Mustang GT", "company": "Ford", "country": "🇺🇸 USA",
        "year": "1964", "topspeed": "250 km/h", "engine": "5.0L V8 Coyote",
        "horsepower": "450 HP", "price": "$42,000", "type": "Muscle Car",
        "info": "American muscle icon with roaring V8 engine",
        "image": "https://editorial.pxcrush.net/carsales/general/editorial/2024-ford-mustang-gt-fastback-auto-45.jpg"
    },
    
    # Lamborghini Models
    "lamborghini huracan": {
        "name": "Lamborghini Huracán", "company": "Lamborghini", "country": "🇮🇹 Italy",
        "year": "2014", "topspeed": "325 km/h", "engine": "5.2L V10",
        "horsepower": "640 HP", "price": "$261,000", "type": "Supercar",
        "info": "Italian bull with screaming V10 and sharp design",
        "image": "https://images.pexels.com/photos/17632045/pexels-photo-17632045.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "lamborghini aventador": {
        "name": "Lamborghini Aventador", "company": "Lamborghini", "country": "🇮🇹 Italy",
        "year": "2011", "topspeed": "350 km/h", "engine": "6.5L V12",
        "horsepower": "770 HP", "price": "$500,000", "type": "Hypercar",
        "info": "V12 monster with scissor doors and explosive performance",
        "image": "https://images.pexels.com/photos/11191242/pexels-photo-11191242.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    
    # Porsche Models
    "porsche 911": {
        "name": "Porsche 911 Turbo S", "company": "Porsche", "country": "🇩🇪 Germany",
        "year": "1963", "topspeed": "330 km/h", "engine": "3.8L Flat-6 Turbo",
        "horsepower": "640 HP", "price": "$216,000", "type": "Sports Car",
        "info": "Iconic sports car with rear-engine layout",
        "image": "https://hips.hearstapps.com/hmg-prod/images/2025-porsche-911-carrera-gts-145-68af3df4bea4b.jpg"
    },
    
    # Ferrari Models
    "ferrari sf90": {
        "name": "Ferrari SF90 Stradale", "company": "Ferrari", "country": "🇮🇹 Italy",
        "year": "2019", "topspeed": "340 km/h", "engine": "4.0L V8 Hybrid",
        "horsepower": "986 HP", "price": "$625,000", "type": "Hypercar",
        "info": "First series-production plug-in hybrid Ferrari",
        "image": "https://images.pexels.com/photos/12801144/pexels-photo-12801144.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    
    # Audi Models
    "audi r8": {
        "name": "Audi R8 V10", "company": "Audi", "country": "🇩🇪 Germany",
        "year": "2006", "topspeed": "331 km/h", "engine": "5.2L V10",
        "horsepower": "602 HP", "price": "$170,000", "type": "Supercar",
        "info": "Everyday supercar with Quattro all-wheel drive",
        "image": "https://images.pexels.com/photos/10566898/pexels-photo-10566898.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    
    # McLaren Models
    "mclaren 720s": {
        "name": "McLaren 720S", "company": "McLaren", "country": "🇬🇧 UK",
        "year": "2017", "topspeed": "341 km/h", "engine": "4.0L V8 Twin-Turbo",
        "horsepower": "710 HP", "price": "$300,000", "type": "Supercar",
        "info": "British engineering with dihedral doors",
        "image": "https://images.pexels.com/photos/10550012/pexels-photo-10550012.jpeg?auto=compress&cs=tinysrgb&w=800"
    }
}

# Get all car names for search suggestions
ALL_CARS = list(CAR_DATABASE.keys())

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🏎️ Ultimate Sports Cars Database</title>
    <style>
        /* Bright Background with Sports Car */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 1100px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.95)), 
                        url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #333;
            min-height: 100vh;
        }
        
        /* Modern Container */
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 25px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Header with Gradient */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid linear-gradient(90deg, #ff6b6b, #4dabf7, #ffd166);
            background: linear-gradient(90deg, #ff6b6b, #4dabf7, #ffd166);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h1 {
            font-size: 3.5em;
            margin: 0;
            background: linear-gradient(90deg, #ff6b6b, #4dabf7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Search Section */
        .search-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 35px;
            border-radius: 20px;
            margin: 30px 0;
            color: white;
            text-align: center;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        }
        
        .search-input {
            width: 70%;
            padding: 18px 25px;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            background: rgba(255,255,255,0.95);
            color: #333;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            margin: 15px 0;
            transition: all 0.3s;
        }
        
        .search-input:focus {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }
        
        .search-btn {
            background: linear-gradient(45deg, #ff6b6b, #ff5252);
            color: white;
            padding: 18px 50px;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin: 20px 0;
            transition: all 0.3s;
            box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
        }
        
        .search-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 30px rgba(255, 107, 107, 0.4);
        }
        
        /* Car Display Card */
        .car-card {
            background: white;
            border-radius: 20px;
            padding: 35px;
            margin: 40px 0;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: transform 0.3s;
        }
        
        .car-card:hover {
            transform: translateY(-10px);
        }
        
        .car-image {
            width: 100%;
            max-width: 500px;
            border-radius: 15px;
            margin: 20px auto;
            display: block;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            border: 3px solid #4dabf7;
        }
        
        /* Specs Grid */
        .specs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .spec-item {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #4dabf7;
        }
        
        /* Company Tags */
        .company-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin: 30px 0;
        }
        
        .company-tag {
            background: linear-gradient(45deg, #4dabf7, #228be6);
            color: white;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .company-tag:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 20px rgba(77, 171, 247, 0.3);
        }
        
        /* Stats Bar */
        .stats-bar {
            background: linear-gradient(90deg, #ff6b6b, #4dabf7);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 30px 0;
            display: flex;
            justify-content: space-around;
            text-align: center;
        }
        
        .logout-btn {
            position: absolute;
            top: 30px;
            right: 30px;
            background: #ff6b6b;
            color: white;
            padding: 12px 25px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        }
        
        /* Car Suggestion Chips */
        .suggestion-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin: 25px 0;
        }
        
        .chip {
            background: #4dabf7;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .chip:hover {
            background: #228be6;
            transform: translateY(-3px);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .container { padding: 20px; }
            h1 { font-size: 2.5em; }
            .search-input { width: 90%; }
            .specs-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <a href="/logout" class="logout-btn">Logout</a>
    
    <div class="container">
        <div class="header">
            <h1>🏎️ ULTIMATE SPORTS CARS DATABASE</h1>
            <p style="font-size: 1.2em; opacity: 0.8;">Welcome, {{ username }}! | Server: {{ hostname }}</p>
        </div>
        
        <!-- Stats Bar -->
        <div class="stats-bar">
            <div>
                <h3 style="margin: 0; font-size: 2em;">{{ total_cars }}</h3>
                <p>Premium Cars</p>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 2em;">{{ total_companies }}</h3>
                <p>Brands</p>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 2em;">{{ total_countries }}</h3>
                <p>Countries</p>
            </div>
        </div>
        
        <!-- Search Section -->
        <div class="search-section">
            <h2 style="color: white; margin-top: 0;">🔍 SEARCH ANY SPORTS CAR</h2>
            <form method="POST">
                <input type="text" name="carname" class="search-input" 
                       placeholder="Type car name (e.g., 'bmw m5', 'lamborghini huracan', 'tesla model s')" 
                       required
                       list="car-suggestions">
                <datalist id="car-suggestions">
                    {% for car in all_cars %}
                    <option value="{{ car }}">
                    {% endfor %}
                </datalist>
                <br>
                <button type="submit" class="search-btn">🚀 GET DETAILED SPECIFICATIONS</button>
            </form>
            
            <!-- Quick Suggestions -->
            <div class="suggestion-chips">
                {% for chip in suggestion_chips %}
                <span class="chip" onclick="document.getElementsByName('carname')[0].value='{{ chip }}'; document.forms[0].submit();">
                    {{ chip }}
                </span>
                {% endfor %}
            </div>
        </div>
        
        <!-- Company Tags -->
        <div style="text-align: center; margin: 40px 0;">
            <h3>🏢 EXPLORE BY BRAND</h3>
            <div class="company-tags">
                <span class="company-tag" onclick="searchByCompany('BMW')">🇩🇪 BMW</span>
                <span class="company-tag" onclick="searchByCompany('Tesla')">🇺🇸 Tesla</span>
                <span class="company-tag" onclick="searchByCompany('Lamborghini')">🇮🇹 Lamborghini</span>
                <span class="company-tag" onclick="searchByCompany('Mercedes')">🇩🇪 Mercedes</span>
                <span class="company-tag" onclick="searchByCompany('Ferrari')">🇮🇹 Ferrari</span>
                <span class="company-tag" onclick="searchByCompany('Porsche')">🇩🇪 Porsche</span>
                <span class="company-tag" onclick="searchByCompany('Tata')">🇮🇳 Tata</span>
                <span class="company-tag" onclick="searchByCompany('Mahindra')">🇮🇳 Mahindra</span>
                <span class="company-tag" onclick="searchByCompany('Ford')">🇺🇸 Ford</span>
                <span class="company-tag" onclick="searchByCompany('Audi')">🇩🇪 Audi</span>
                <span class="company-tag" onclick="searchByCompany('McLaren')">🇬🇧 McLaren</span>
            </div>
        </div>
        
        <!-- Car Display -->
        {% if car_info %}
        <div class="car-card">
            <h2 style="text-align: center; color: #4dabf7; font-size: 2.5em;">🎯 {{ car_info.name }}</h2>
            <div style="text-align: center;">
                <img src="{{ car_info.image }}" alt="{{ car_info.name }}" class="car-image">
            </div>
            
            <div class="specs-grid">
                <div class="spec-item">
                    <strong>🏭 MANUFACTURER</strong><br>
                    {{ car_info.company }} {{ car_info.country }}
                </div>
                <div class="spec-item">
                    <strong>📅 LAUNCH YEAR</strong><br>
                    {{ car_info.year }}
                </div>
                <div class="spec-item">
                    <strong>⚡ TOP SPEED</strong><br>
                    {{ car_info.topspeed }}
                </div>
                <div class="spec-item">
                    <strong>🔧 ENGINE</strong><br>
                    {{ car_info.engine }}
                </div>
                <div class="spec-item">
                    <strong>🐎 HORSEPOWER</strong><br>
                    {{ car_info.horsepower }}
                </div>
                <div class="spec-item">
                    <strong>💰 PRICE</strong><br>
                    {{ car_info.price }}
                </div>
                <div class="spec-item">
                    <strong>🏷️ TYPE</strong><br>
                    {{ car_info.type }}
                </div>
                <div class="spec-item">
                    <strong>🖥️ SERVER</strong><br>
                    {{ hostname }}
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; margin: 25px 0;">
                <h3 style="color: #333; margin-top: 0;">📖 DESCRIPTION</h3>
                <p style="font-size: 1.1em; line-height: 1.6;">{{ car_info.info }}</p>
            </div>
            
            <p style="text-align: center; color: #666; font-size: 0.9em;">
                <strong>🕒 QUERIED AT:</strong> {{ timestamp }}
            </p>
        </div>
        {% endif %}
        
        {% if error %}
        <div style="background: #ffeaea; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #ff6b6b;">
            <h2 style="color: #ff6b6b;">❌ CAR NOT FOUND!</h2>
            <p style="font-size: 1.1em;">Try one of these popular sports cars:</p>
            <div class="suggestion-chips">
                {% for car in sample_cars %}
                <span class="chip" onclick="document.getElementsByName('carname')[0].value='{{ car }}'; document.forms[0].submit();">
                    {{ car }}
                </span>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
    
    <script>
    function searchByCompany(company) {
        const carsByCompany = {
            'BMW': ['bmw m5', 'bmw i8'],
            'Tesla': ['tesla model s', 'tesla roadster'],
            'Lamborghini': ['lamborghini huracan', 'lamborghini aventador'],
            'Mercedes': ['mercedes amg gt'],
            'Ferrari': ['ferrari sf90'],
            'Porsche': ['porsche 911'],
            'Tata': ['tata nexon'],
            'Mahindra': ['mahindra thar'],
            'Ford': ['ford mustang gt'],
            'Audi': ['audi r8'],
            'McLaren': ['mclaren 720s']
        };
        
        if (carsByCompany[company]) {
            // Show first car from company
            document.getElementsByName('carname')[0].value = carsByCompany[company][0];
            document.forms[0].submit();
        }
    }
    
    // Auto-focus search input
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementsByName('carname')[0].focus();
    });
    </script>
</body>
</html>
'''

# Login Page
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Sports Cars Database</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 90%;
            max-width: 500px;
            backdrop-filter: blur(10px);
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .tagline {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .input-group {
            margin: 20px 0;
        }
        
        input {
            width: 100%;
            padding: 18px;
            margin: 10px 0;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            box-sizing: border-box;
            transition: all 0.3s;
        }
        
        input:focus {
            border-color: #4dabf7;
            box-shadow: 0 0 0 3px rgba(77, 171, 247, 0.2);
            outline: none;
        }
        
        .login-btn {
            background: linear-gradient(45deg, #ff6b6b, #ff5252);
            color: white;
            padding: 18px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s;
        }
        
        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255, 107, 107, 0.3);
        }
        
        .credentials {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            color: #333;
        }
        
        .error {
            background: #ffeaea;
            color: #ff6b6b;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border: 1px solid #ffcccc;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #4dabf7;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔐 SPORTS CARS DATABASE</h1>
        <p class="tagline">Access the world's most comprehensive sports cars collection</p>
        
        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="👤 Username" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="🔒 Password" required>
            </div>
            
            <button type="submit" class="login-btn">ACCESS PREMIUM DATABASE</button>
        </form>
        
        {% if error %}
        <div class="error">
            ❌ Invalid credentials! Use: admin / password
        </div>
        {% endif %}
        
        <div class="credentials">
            <p><strong>Demo Credentials:</strong></p>
            <p>👤 Username: <strong>admin</strong></p>
            <p>🔒 Password: <strong>password</strong></p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{{ total_cars }}</div>
                <div>Premium Cars</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_companies }}</div>
                <div>Brands</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_countries }}</div>
                <div>Countries</div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login_page():
    # Calculate statistics
    companies = set(car['company'] for car in CAR_DATABASE.values())
    countries = set(car['country'] for car in CAR_DATABASE.values())
    
    if 'username' in session:
        return redirect('/portal')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == LOGIN_CREDENTIALS['username'] and password == LOGIN_CREDENTIALS['password']:
            session['username'] = username
            return redirect('/portal')
        else:
            return render_template_string(LOGIN_TEMPLATE, 
                                       error=True,
                                       total_cars=len(CAR_DATABASE),
                                       total_companies=len(companies),
                                       total_countries=len(countries))
    
    return render_template_string(LOGIN_TEMPLATE, 
                               error=False,
                               total_cars=len(CAR_DATABASE),
                               total_companies=len(companies),
                               total_countries=len(countries))

@app.route('/portal', methods=['GET', 'POST'])
def car_portal():
    if 'username' not in session:
        return redirect('/')
    
    # Calculate statistics
    companies = set(car['company'] for car in CAR_DATABASE.values())
    countries = set(car['country'] for car in CAR_DATABASE.values())
    hostname = os.uname().nodename
    
    # Sample cars for suggestions
    sample_cars = ["bmw m5", "lamborghini huracan", "tesla model s", 
                   "ferrari sf90", "porsche 911", "mclaren 720s"]
    suggestion_chips = ["bmw m5", "tesla model s", "lamborghini huracan", 
                       "porsche 911", "ferrari sf90", "audi r8"]
    
    if request.method == 'POST':
        carname = request.form['carname'].lower().strip()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if carname in CAR_DATABASE:
            car_info = CAR_DATABASE[carname]
            return render_template_string(HTML_TEMPLATE, 
                                       car_info=car_info,
                                       error=None,
                                       timestamp=timestamp,
                                       hostname=hostname,
                                       username=session['username'],
                                       total_cars=len(CAR_DATABASE),
                                       total_companies=len(companies),
                                       total_countries=len(countries),
                                       all_cars=ALL_CARS,
                                       sample_cars=sample_cars,
                                       suggestion_chips=suggestion_chips)
        else:
            return render_template_string(HTML_TEMPLATE, 
                                       car_info=None,
                                       error=True,
                                       timestamp=timestamp,
                                       hostname=hostname,
                                       username=session['username'],
                                       total_cars=len(CAR_DATABASE),
                                       total_companies=len(companies),
                                       total_countries=len(countries),
                                       all_cars=ALL_CARS,
                                       sample_cars=sample_cars,
                                       suggestion_chips=suggestion_chips)
    
    return render_template_string(HTML_TEMPLATE, 
                               car_info=None,
                               error=None,
                               timestamp=None,
                               hostname=hostname,
                               username=session['username'],
                               total_cars=len(CAR_DATABASE),
                               total_companies=len(companies),
                               total_countries=len(countries),
                               all_cars=ALL_CARS,
                               sample_cars=sample_cars,
                               suggestion_chips=suggestion_chips)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    print("🚀 Starting Sports Cars Database on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
