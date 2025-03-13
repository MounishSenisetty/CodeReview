const vscode = require('vscode');
const axios = require('axios');

const API_KEY = 'AIzaSyBJuSTfgV3RTOlHe59MH6zDfwS-Ve4pnIo';
const API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + API_KEY;
const Prompt = `You are an expert AI Code Reviewer and Security Auditor. Your task is to analyze the following code snippet for:

1️⃣ *Security Vulnerabilities*:
   - Identify and explain possible security risks such as:
     - SQL Injection
     - Cross-Site Scripting (XSS)
     - Hardcoded Secrets (API Keys, Passwords)
     - Buffer Overflows
     - Insecure Cryptographic Practices
     - Insufficient Authentication & Authorization
     - Arbitrary File Access (Path Traversal, LFI/RFI)
     - Memory Management Issues (Use-after-free, Double-Free, etc.)
   - Provide *clear explanations* for each issue and suggest *secure fixes*.

2️⃣ *Code Quality & Best Practices*:
   - Identify *poor coding practices* and suggest *improvements*.
   - Highlight *performance optimizations* and *efficiency improvements*.
   - Ensure *clean coding standards* are followed (e.g., naming conventions, modularity).
   - Highlight redundant or inefficient code and propose *optimized solutions*.

3️⃣ *Static Analysis Findings*:
   - Explain static analysis tool findings and suggest fixes.

---
*📌 Code to Review:*
`;

async function analyzeCode() {  
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        console.log("Editor not activated");
        vscode.window.showErrorMessage("No active editor found!");
        return;
    }

    const code = editor.document.getText();
    const prompt = Prompt + `\n\n${code} `;

    try {
        const response = await axios.post(API_URL, {
            contents: [{ role: "user", parts: [{ text: prompt }] }]  
        });

        const analysisText = response.data?.candidates?.[0]?.content?.parts?.[0]?.text;
        
        if (!analysisText) {
            throw new Error("Invalid response format from Gemini API");
        }

        vscode.window.showInformationMessage("Analysis of the code complete.");

        // Create and show markdown content
        const doc = await vscode.workspace.openTextDocument({
            content: analysisText,
            language: 'markdown'
        });
        
        // Show the document in a new editor
        await vscode.window.showTextDocument(doc, {
            viewColumn: vscode.ViewColumn.Beside,
            preview: true
        });
        
        // Open the markdown preview
        await vscode.commands.executeCommand('markdown.showPreview', doc.uri);

    } catch (error) {
        console.error("Error details:", error);
        const errorMessage = error.response?.data?.error?.message || error.message;
        vscode.window.showErrorMessage("Error analyzing code: " + errorMessage);
    }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    let disposable = vscode.commands.registerCommand('Finderrors', analyzeCode);
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};