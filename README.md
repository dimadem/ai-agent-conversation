# **AI AGENT CONVERSATION**

#### **requirenments.txt**
[FASTAPI](https://fastapi.tiangolo.com/)

[UVICORN](https://pypi.org/project/uvicorn/)

[OPENAI](https://platform.openai.com/docs/api-reference/responses)

[OPENAI AGENT SDK](https://openai.github.io/openai-agents-python/)

---

### **Setup**

1. собрать проект -> ./setup.sh
2. добавить нужные ключи в .env файл
3. запустить проект -> ./dev.sh

---

### **Описание**

⎿  📁 app
     ├─ 📄 __init__.py
     ├─ 📁 agents                <!-- Агенты для различных задач -->
     │  ├─ 📄 evaluation_agent.py
     │  ├─ 📄 interviewee_agent.py
     │  ├─ 📁 prompts            <!-- Шаблоны и утилиты для агентов -->
     │  │  ├─ 📄 __init__.py
     │  │  ├─ 📄 evaluation_system_prompt.yaml
     │  │  ├─ 📄 persona_system_prompt.yaml
     │  │  ├─ 📄 utils.py
     │  ├─ 📁 tools              <!-- Инструменты для агентов -->
     │  │  ├─ 📄 answer_question.py
     │  │  ├─ 📄 extract_star.py
     ├─ 📁 api                   <!-- API для взаимодействия с фронтендом -->
     │  ├─ 📄 __init__.py
     │  ├─ 📄 evaluation.py
     │  ├─ 📄 interview.py
     ├─ 📁 core                  <!-- Основные конфигурации и константы -->
     │  ├─ 📄 __init__.py
     │  ├─ 📄 config.py
     │  ├─ 📄 constants.py
     │  ├─ 📄 openai.py
     ├─ 📁 frontend              <!-- HTML файлы для фронтенда -->
     │  ├─ 📄 evaluation.html
     │  ├─ 📄 index.html
     │  ├─ 📄 interview.html
     │  ├─ 📄 report.html
     │  ├─ 📄 select-candidate.html
     ├─ 📄 main.py               <!-- Главный файл запуска приложения -->
     ├─ 📁 model                 <!-- Модели для обработки данных -->
     │  ├─ 📄 __init__.py
     │  ├─ 📄 stt.py
     │  ├─ 📄 tts.py
     │  ├─ 📄 ttt.py
     ├─ 📁 utils                 <!-- Утилиты и вспомогательные функции -->
     │  └─ 📄 __init__.py

---

#### **Frontend**

##### index.html
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Server

    User->>Browser: Open main page
    Browser->>Server: Request /select-persona
    Server-->>Browser: Response with select-persona page
    Browser->>User: Display select-persona page

    User->>Browser: Open evaluation page
    Browser->>Server: Request /evaluation
    Server-->>Browser: Response with evaluation page
    Browser->>User: Display evaluation page

    Note right of User: User can navigate between pages
```

---

##### select-candidate.html
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Form as persona-form
    participant Window

    User->>Browser: Load /select-candidate.html
    Browser->>Form: Render form
    User->>Form: Fill in "persona-profile" and "persona-skill"
    User->>Form: Click "Перейти к интервью"
    Form->>Browser: form submit event
    Browser->>Form: preventDefault()
    Form->>Browser: Get "persona-profile" value
    Form->>Browser: Get "persona-skill" value
    Browser->>Window: Redirect to /interview with parameters
    Note right of Window: URL: /interview?persona=<profile>&skill=<skill>
```

---

##### interview.html
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant WebSocketServer

    Note over User,Browser: User opens the interview page
    User->>Browser: Load interview.html
    Browser->>Browser: Parse URL parameters
    Browser->>Browser: Display persona and skill
    Browser->>Browser: Initialize state variables
    Browser->>Browser: Initialize conversation history

    Note over Browser: User clicks "Записать голос" button
    User->>Browser: Click recordButton
    alt isRecording is false
        Browser->>Browser: Start recording
        Browser->>Browser: Set isRecording to true
    else isRecording is true
        Browser->>Browser: Stop recording
        Browser->>Browser: Set isRecording to false
    end

    Note over Browser: WebSocket connection management
    Browser->>WebSocketServer: Connect to WebSocket
    WebSocketServer-->>Browser: WebSocket connection established
    Browser->>Browser: Set isConnected to true
```

---

##### evaluation.html
```mermaid
sequenceDiagram
    participant User as User
    participant Browser as Browser
    participant FileReader as FileReader

    User->>Browser: Open evaluation.html
    Browser->>User: Display form

    User->>Browser: Select JSON file
    Browser->>FileReader: Read file content
    FileReader-->>Browser: Return file content
    Browser->>Browser: Populate textarea with JSON content

    User->>Browser: Submit form
    Browser->>Browser: Validate form data
    alt Valid JSON
        Browser->>User: Display success message
    else Invalid JSON
        Browser->>User: Display error message
    end

    note over Browser: The form includes a file input and a textarea for JSON data.
    note over FileReader: FileReader API is used to read the content of the selected file.
```

---

##### report.html
```mermaid
sequenceDiagram
    participant User as User
    participant Browser as Browser
    participant Server as Server

    User->>Browser: Open report.html
    Browser->>User: Display loading indicator

    note over Browser: Set a timeout for 20 seconds
    Browser->>Browser: setTimeout (20 seconds)
    
    Browser->>Server: fetch('/api/evaluation')
    alt Response received before timeout
        Server-->>Browser: Response with data
        Browser->>Browser: clearTimeout
        Browser->>Browser: Check response status
        alt Response not OK
            Browser->>User: Display server error message
        else Response OK
            Browser->>Browser: Parse JSON data
            alt Data is valid
                Browser->>User: Display data in report
            else Data is invalid
                Browser->>User: Display no data message
            end
        end
    else Timeout occurs
        Browser->>Browser: Timeout function executes
        Browser->>User: Display timeout error message
    end

    note over Browser: Hide loading indicator after receiving response or timeout
```

---

