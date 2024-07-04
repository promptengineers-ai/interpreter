# Python Sandboxed - Code Interpreter

This API allows users to execute Python code in a sandboxed environment, upload files, install packages, and manage sessions. Each session is isolated to ensure that the code, files, and packages do not interfere with other users.

Example curl Request (Verify will error when numpy is not installed):

```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "code": "import os\nimport numpy as np\na = int(os.getenv(\"VAR_A\"))\nb = int(os.getenv(\"VAR_B\"))\nc = int(os.getenv(\"VAR_C\"))\narray = np.array([a, b, c])\nresult = np.sum(array)\nprint(f\"Result of summing [{a}, {b}, {c}] is: {result}\")",
  "env": {
    "VAR_A": "10",
    "VAR_B": "20",
    "VAR_C": "30"
  }
}'

## Result
# {"detail":"Session not found."}
```

Example curl Request (Install numpy and execute the code):

```bash
curl -X POST http://localhost:8000/install -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "packages": ["numpy"]
}'

## Result
# {"status":"success","installed_packages":["numpy"]}
```

Execute numpy with Env vars

```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "code": "import os\nimport numpy as np\na = int(os.getenv(\"VAR_A\"))\nb = int(os.getenv(\"VAR_B\"))\nc = int(os.getenv(\"VAR_C\"))\narray = np.array([a, b, c])\nresult = np.sum(array)\nprint(f\"Result of summing [{a}, {b}, {c}] is: {result}\")",
  "env": {
    "VAR_A": "10",
    "VAR_B": "20",
    "VAR_C": "30"
  }
}'

## Result
# {"status":"success","output":"Result of summing [10, 20, 30] is: 60\n","errors":""}
```

Example curl Request (Verify numpy has been uninstalled):

```bash
curl -X POST http://localhost:8000/terminate -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id"
}'

## Result
# {"status":"success","message":"Session your_session_id terminated successfully."}

curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "code": "import os\nimport numpy as np\na = int(os.getenv(\"VAR_A\"))\nb = int(os.getenv(\"VAR_B\"))\nc = int(os.getenv(\"VAR_C\"))\narray = np.array([a, b, c])\nresult = np.sum(array)\nprint(f\"Result of summing [{a}, {b}, {c}] is: {result}\")",
  "env": {
    "VAR_A": "10",
    "VAR_B": "20",
    "VAR_C": "30"
  }
}'

## Result
# {"detail":"Session not found."}
```

### Execute against files

Upload a file for a specific session.

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "session_id=your_session_id" \
  -F "file=@data/AAPL.csv"

## Result
# {"filename":"AAPL.csv","location":"/tmp/your_session_id/AAPL.csv"}
```

Install pandas pacakage for created session to interact with csv.

```bash
curl -X POST http://localhost:8000/install -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "packages": ["pandas"]
}'

## Result
# {"status":"success","installed_packages":["pandas"]}
```

Execute to interact with csv

```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id",
  "code": "import pandas as pd\nfile_path = \"/tmp/your_session_id/AAPL.csv\"\ndf = pd.read_csv(file_path)\nfirst_row = df.iloc[0]\nprint(first_row.to_json())"
}'

## Result
# {"status":"success","output":"{\"Date\":\"2022-03-16\",\"Open\":157.050003,\"High\":160.0,\"Low\":154.460007,\"Close\":159.589996,\"Adj Close\":158.629059,\"Volume\":102300200}\n","errors":""}
```

Terminate session to uninstall pacakges and remove files.

```bash
curl -X POST http://localhost:8000/terminate -H "Content-Type: application/json" -d '{
  "session_id": "your_session_id"
}'

## Result
# {"status":"success","message":"Session your_session_id terminated successfully."}
```