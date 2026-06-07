# Railway Deployment Plan

Deploying this local MCP Server to [Railway](https://railway.app/) requires addressing two major things: **Terminal Interactivity** and **Secret Management**.

Because Railway runs your application in the cloud without an interactive terminal and handles ephemeral deployments, we cannot use local `.json` files for secrets or prompt the user via `stdin`.

Here is the step-by-step plan to prepare and deploy the server.

## 1. Remove or Bypass the Terminal Approval
Currently, `server.py` pauses and asks `Approve? (y/n)` in the terminal. On Railway, this will throw an `EOFError` (as there is no active terminal) and fail the request.

**Solution**:
Introduce an environment variable (e.g., `ENVIRONMENT=production`) to bypass the terminal prompt, and instead secure the endpoints with a static API Key.
- Update `server.py` to check for a custom `X-API-Key` header.
- Skip `input()` if running in the cloud.

## 2. Migrate Secrets to Environment Variables
You should **NEVER** commit `credentials.json` or `token.json` to your Git repository. 

**Solution**:
- Keep `credentials.json` and `token.json` in your `.gitignore` (already done).
- Update `auth.py` to read credentials directly from environment variables.
- You can store the raw JSON strings of both files into Railway environment variables:
  - `GOOGLE_CREDENTIALS_JSON`
  - `GOOGLE_TOKEN_JSON`

## 3. Update the Port Configuration
Railway injects a dynamic `$PORT` environment variable that your app must bind to.

**Solution**:
Update the bottom of `server.py`:
```python
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## 4. Deployment Steps

Once the code changes are made, deploying to Railway is straightforward:

1. **Commit your code to GitHub**: Push the repository (ensure `.gitignore` is intact).
2. **Connect Railway to GitHub**: In the Railway dashboard, create a new project and select "Deploy from GitHub repo".
3. **Add Environment Variables**: Before the deployment finishes, go to the Railway project variables and add:
   - `PORT`: (Railway usually handles this, but good to know)
   - `ENVIRONMENT`: `production`
   - `API_KEY`: `<generate a secret string to act as your password>`
   - `GOOGLE_CREDENTIALS_JSON`: `<paste the exact contents of credentials.json>`
   - `GOOGLE_TOKEN_JSON`: `<paste the exact contents of token.json>`
4. **Deploy**: Railway will automatically detect `requirements.txt`, install dependencies, and start the app using the command it finds or fallback to the python execution.

---
**Do you want me to go ahead and make the code changes for Steps 1, 2, and 3 so it is ready for deployment?**
