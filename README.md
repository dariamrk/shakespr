# Shakespr - AI-Powered Relocation Assistant
> To be, or not to be, that is the question.

## Overview
Shakespr is a Telegram bot designed to help people make informed decisions about international relocation. It provides real-world cost of living data, lifestyle comparisons, and personalized recommendations to help users evaluate potential destinations.

## Features
- Basic city information retrieval from Numbeo
- Cost of living comparisons
- Simple user profile management
- Data persistence in PostgreSQL


- City quality-of-life scoring
- Salary and purchasing power analysis
- Career opportunity evaluation
- Multi-language support
- Interactive data visualization
- AI-powered personalized recommendations

## Proposed System Architecture
The following diagrams represent potential future architecture designs that we're considering. These are preliminary proposals and may evolve based on feedback and project needs.

### Core System Components
```mermaid
flowchart TB
    %% Client Layer
    TG[Telegram Bot API]
    WH[Webhook Handler]

    %% Application Layer
    API[FastAPI Service]
    CS[City Service]
    US[User Service]
    AS[Analysis Service]
    TS[Translation Service]
    MR[Message Router]
    CMD[Command Processor]
    DH[Dialog Handler]

    %% AI Layer
    LLM[LLM Service]
    RAG[RAG Engine]
    NLP[NLP Service]

    %% Data Layer
    PG[(PostgreSQL)]
    VEC[(PGVector)]
    RD[(Redis)]

    %% Connections
    TG --> WH
    WH --> API
    API --> CS & US & AS & TS
    API --> MR
    MR --> CMD & DH
    CS & US & AS --> LLM & RAG & NLP
    LLM & RAG & NLP --> PG & VEC
    CS & US & AS --> RD
```

### Data Collection and Processing
```mermaid
flowchart TB
    %% Data Collection
    NS[Numbeo Scraper]
    SS[Salary Scraper]
    JS[Job Market Scraper]
    QS[Quality of Life Scraper]
    
    %% Data Processing
    DP[Data Preprocessor]
    NC[Normalization Component]
    VC[Validation Component]
    
    %% Analytics
    COL[Cost Calculator]
    QOL[Quality Scorer]
    PP[Purchase Power Analyzer]
    JA[Job Analyzer]
    
    %% Task Management
    CW[Celery Workers]
    SC[Scheduler]
    MQ[Message Queue]
    
    %% Connections
    NS & SS & JS & QS --> DP
    DP --> NC --> VC
    VC --> COL & QOL & PP & JA
    COL & QOL & PP & JA --> MQ
    MQ --> CW
    SC --> NS & SS & JS & QS
```

### Data Flow Examples
#### City Comparison   
```mermaid
sequenceDiagram
    participant U as User
    participant B as Bot
    participant A as API
    participant C as Cache
    participant D as DB
    participant L as LLM
    participant S as Scraper

    U->>B: Request comparison
    B->>A: Forward request
    A->>C: Check cache
    alt Cache hit
        C-->>A: Return cached data
    else Cache miss
        A->>D: Check database
        alt Fresh data exists
            D-->>A: Return data
        else Stale or missing
            A->>S: Request new data
            S-->>A: Return scraped data
            A->>D: Store data
            A->>C: Update cache
        end
    end
    A->>L: Generate analysis
    L-->>A: Return analysis
    A->>B: Send response
    B->>U: Display result
```
#### RAG-based Recommendation
```mermaid
sequenceDiagram
    participant U as User
    participant B as Bot
    participant A as API
    participant V as VectorDB
    participant L as LLM
    participant D as DB

    U->>B: Ask for advice
    B->>A: Process request
    A->>V: Query embedding
    V-->>A: Return contexts
    A->>D: Get user prefs
    D-->>A: Return user data
    A->>L: Generate response
    L-->>A: Return recommendation
    A->>B: Format response
    B->>U: Show advice
```

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Telegram Bot Token

### Local Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/shakespr.git
cd shakespr
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up databases
```bash
# Create necessary databases
python scripts/setup_db.py

# Initialize schemas
psql -d user_data -f sql/user_data/schema/init.sql
psql -d numbeo_data -f sql/numbeo_data/schema/init.sql
```

5. Configure environment variables
```bash
# Copy example environment file
cp config/_env config/.env

# Edit .env with your settings
nano config/.env
```

6. Run the bot
```bash
python run_bot.py
```

## Contributing

We welcome contributions! Here's how you can help:

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (once implemented)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Areas for Contribution
- Adding new data sources
- Implementing planned features
- Improving data visualization
- Adding tests
- Documentation improvements
- Bug fixes
- Performance optimizations

### Code Style
- Follow PEP 8 guidelines
- Include docstrings for new functions and classes
- Add type hints
- Write meaningful commit messages

## Technical Considerations

### Current Stack
- Python Telegram Bot API
- PostgreSQL for data storage
- Beautiful Soup for web scraping
- Python-dotenv for configuration

### Proposed Future Stack
- FastAPI for API layer
- Redis for caching
- LangChain for RAG implementation
- pgvector for vector storage
- Celery for task management
- Plotly/D3.js for data visualization


---

**Note**: This README reflects the current state of the project and potential future developments. The proposed architecture and features are preliminary and subject to change based on feedback and project requirements.
