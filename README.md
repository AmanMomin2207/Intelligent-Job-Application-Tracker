#  Intelligent Job Application Tracker & Analyzer

A full-stack intelligent system that tracks job applications and analyzes resumes/job descriptions using NLP, PySpark, and a distributed AWS-based cloud architecture.
It identifies skill gaps, calculates match scores, and recommends better job opportunities.

# Overview

The Intelligent Job Application Tracker & Analyzer helps job seekers streamline their job-search workflow by:

Tracking all job applications in one place

Analyzing resume content

Matching resumes against job descriptions

Highlighting missing skills

Providing insights to improve resumes and job targeting

The project uses a hybrid architecture combining Next.js, Spring Boot, PySpark, and AWS services.

#  Features
## 1. Resume Upload & Parsing

Upload PDF/DOCX resumes

Extract text using NLP + PySpark

Convert extracted content to structured JSON (stored in MongoDB)

## 2. Job Description Analysis

Add job links or paste job descriptions

Extract required skills, keywords, important phrases

Store job details in PostgreSQL

## 3. Resume vs Job Matching

PySpark calculates:

Match percentage

Missing skills

Important keywords

Recommendations for improvement

## 4. Job Application Tracking

Track applied jobs

Status updates:

Applied

Interview

Rejected

Offer

Filter jobs by status/company

## 5. Admin Dashboard

View all uploaded resumes

Monitor NLP processing pipeline

Browse all job applications and match results

## 6. Cloud-Based Processing

Resume files stored in AWS S3

Upload triggers AWS Lambda → EMR PySpark job

Processed results stored in MongoDB & PostgreSQL

# Tech Stack
## Frontend

Next.js

Job list UI

Analytics dashboard

Resume viewer

Filters, charts, match scores

## Backend

Spring Boot (Java)

RESTful CRUD APIs

Authentication

Connects to PostgreSQL & MongoDB

Processing Layer

## PySpark

Resume parsing

Keyword extraction

JD–resume matching

NLP (TF-IDF, cosine similarity, ML models)

## Databases

PostgreSQL – job data

MongoDB – parsed resume JSON

## AWS Infrastructure

S3 – resume storage

RDS – PostgreSQL

EMR – PySpark jobs

Lambda – triggers Spark pipeline automatically

# How It Works (Architecture Flow)
## 1. User Uploads Resume

Resume uploaded through Next.js frontend

File stored in AWS S3

## 2. AWS Lambda Trigger

S3 upload triggers Lambda

Lambda triggers EMR Spark job

## 3. PySpark Resume Processing

EMR Spark pipeline runs:

Text extraction

NLP preprocessing

Skill & keyword extraction

JSON generation

JSON saved in MongoDB

## 4. Job Description Storage

User provides job links or descriptions

Parsed & stored in PostgreSQL

## 5. Resume–JD Matching

PySpark calculates:

Match score

Skill gaps

Keyword overlap

Results saved in PostgreSQL

## 6. Frontend Visualization

Next.js dashboard displays:

Match percentage

Missing skills

Resume insights

Job timeline & application tracking

# Completed Work Till Now
## 1. Streamlit GUI Prototype Created
    
Demonstrates NLP workflow

Shows resume parsing & skill extraction

Acts as POC for ML pipeline

## 2. Repository Structure Organized

Added folders for backend, frontend, PySpark processing

Initial documentation prepared

## 3. Sample Resume Parsing (Local)

Resume text extraction

Preprocessing pipeline

Keyword extraction demo

## 4. Research Completed

Explored JD–resume matching techniques

Finalized TF-IDF + cosine similarity approach

Designed AWS pipeline (S3 → Lambda → EMR → Databases)

## 5. Initial Database Schema Drafted

Mongo schema for resume JSON

PostgreSQL schema for job applications
