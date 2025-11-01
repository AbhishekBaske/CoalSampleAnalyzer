#!/usr/bin/env python3
"""
Build script to convert Flask templates to static HTML for Netlify
"""
import os
import shutil
from pathlib import Path
import json

def create_static_build():
    """Create static version of the Flask app for Netlify"""
    
    # Create build directory
    build_dir = Path("static_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Copy static assets
    if Path("static").exists():
        shutil.copytree("static", build_dir / "static")
    
    # Copy dataset images
    if Path("dataset").exists():
        shutil.copytree("dataset", build_dir / "dataset")
    
    # Create main index.html
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coal Spontaneous Combustion Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Coal Analyzer</a>
            <div class="navbar-nav">
                <a class="nav-link" href="#manual">Manual Analysis</a>
                <a class="nav-link" href="#thermal">Thermal Analysis</a>
                <a class="nav-link" href="#batch">Batch Analysis</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <div class="alert alert-info">
                    <h4>⚠️ Migration Notice</h4>
                    <p>This Coal Spontaneous Combustion Analyzer has been converted to a static demo.</p>
                    <p>For full functionality including image processing and thermal analysis, please:</p>
                    <ul>
                        <li>Deploy the Flask app to <strong>Heroku</strong>, <strong>Railway</strong>, or <strong>Render</strong></li>
                        <li>Or run locally using: <code>python app.py</code></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5>Manual Coal Analysis</h5>
                    </div>
                    <div class="card-body">
                        <p>Upload coal images for manual analysis including:</p>
                        <ul>
                            <li>Risk Assessment</li>
                            <li>Coal Type Classification</li>
                            <li>Safety Recommendations</li>
                        </ul>
                        <button class="btn btn-primary" disabled>Upload Image (Demo)</button>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5>Thermal Analysis</h5>
                    </div>
                    <div class="card-body">
                        <p>Advanced thermal simulation and analysis:</p>
                        <ul>
                            <li>Heat Distribution Mapping</li>
                            <li>Combustion Risk Prediction</li>
                            <li>Environmental Factor Analysis</li>
                        </ul>
                        <button class="btn btn-warning" disabled>Analyze Thermal (Demo)</button>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5>Batch Processing</h5>
                    </div>
                    <div class="card-body">
                        <p>Process multiple coal samples:</p>
                        <ul>
                            <li>Bulk Analysis</li>
                            <li>Comparative Reports</li>
                            <li>Statistical Analysis</li>
                        </ul>
                        <button class="btn btn-success" disabled>Batch Process (Demo)</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <h3>Sample Coal Images</h3>
                <div class="row" id="coal-gallery">
                    <!-- Images will be loaded here -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Load sample images
        const coalImages = [
            '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg',
            '100.jpg', '102.jpg', '106.jpg', '107.jpg', '112.png',
            '113.jpg', '119.jpg', '120.jpg', '121.jpg', '122.jpg'
        ];

        const gallery = document.getElementById('coal-gallery');
        coalImages.forEach(img => {
            const col = document.createElement('div');
            col.className = 'col-md-3 mb-3';
            col.innerHTML = `
                <div class="card">
                    <img src="dataset/${img}" class="card-img-top" alt="Coal Sample" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h6 class="card-title">${img}</h6>
                        <button class="btn btn-sm btn-outline-primary" disabled>Analyze (Demo)</button>
                    </div>
                </div>
            `;
            gallery.appendChild(col);
        });
    </script>
</body>
</html>
    """
    
    # Write index.html
    with open(build_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html.strip())
    
    print("✅ Static build created successfully!")
    print(f"📁 Build directory: {build_dir}")
    print("🚀 Ready for Netlify deployment!")

if __name__ == "__main__":
    create_static_build()