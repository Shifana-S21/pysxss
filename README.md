# WAF Evasion for XSS: A Practical Study

This repository contains a Python script and a sample web application designed to demonstrate how character-based Web Application Firewall (WAF) filters for Cross-Site Scripting (XSS) can be bypassed.

### ⚠️ Disclaimer
This project is for **educational and research purposes only**. The techniques described here should only be used in a controlled environment and on applications you are authorized to test. Unauthorized attacks on web applications are illegal.

---

### Step 1: Research on WAFs and XSS Filtering

#### What is a WAF?
A Web Application Firewall (WAF) acts as a reverse proxy, sitting in front of a web application to monitor and filter HTTP/S traffic. Its primary goal is to protect the application from common web-based attacks like SQL Injection, Cross-Site Scripting (XSS), File Inclusion, and others.

#### How Do WAFs Filter XSS?
Many WAFs, especially simpler or older ones, rely on a **negative security model** (blacklisting). They look for specific patterns, keywords, and characters commonly used in attacks. For XSS, these often include:

*   **HTML Tags:** `<script>`, `<img>`, `<body>`, `<svg>`
*   **JavaScript Events:** `onerror`, `onload`, `onmouseover`, `onclick`
*   **JavaScript Keywords:** `alert`, `document`, `window`, `eval`
*   **Special Characters:** `<`, `>`, `'`, `"`, `(`, `)`

If a WAF detects these strings in user input (like a URL parameter or a form field), it will block the request.

#### Evasion Techniques
Attackers bypass these filters by obfuscating their payloads in ways the WAF's blacklist doesn't anticipate. Common techniques include:

1.  **Case Variation:** Using a mix of upper and lower case letters (e.g., `<sCrIpT>`). Some naive regex filters are case-sensitive.
2.  **Encoding:** Using URL, Hex, or HTML entity encoding to represent forbidden characters (e.g., `<` becomes `%3C` or `<`).
3.  **Using Alternative Tags/Events:** A WAF might block `onerror` but not `onload` or `onfocus`. It might block `<script>` but not `<svg>` or `<details>`.
4.  **Obfuscation with Comments:** Breaking up keywords with comments (e.g., `<scr<!-- -->ipt>`).
5.  **Using String Manipulation in JavaScript:** Building the malicious code from characters to avoid keywords. For example, using `String.fromCharCode(97, 108, 101, 114, 116, 40, 49, 41)` instead of `alert(1)`.
6.  **Template Literals:** Using backticks (`` ` ``) in JavaScript can sometimes bypass quote filters.

---

### Step 2: The Payload Generation Script

The `payload_generator.py` script takes a basic JavaScript payload (like `alert('XSS')`) and applies several of the evasion techniques mentioned above to generate a list of potential bypass payloads.

**To Run the Script:**
```bash
python payload_generator.py
```

It will output a list of payloads ready to be tested.

---

### Step 3: The Test Environment

The `sample_app.py` is a simple web application built with Flask. It includes a basic, simulated WAF that filters common XSS keywords.

**The Vulnerability:**
The application has a search page at `/search`. The search term from the `query` parameter is reflected back to the page, which is a classic scenario for Reflected XSS.

**The Simulated WAF:**
The `simple_waf_filter` function in the script looks for and removes the following substrings from the input:
*   `<script`
*   `alert`
*   `onerror`
*   `>`
*   `<`

This WAF is intentionally simple to demonstrate the principle of character-based filtering.

**Setup and Running the Test App:**
1. Install Flask:
   ```bash
   pip install Flask
   ```
2. Run the application:
   ```bash
   python sample_app.py
   ```
3. Open your web browser and go to `http://127.0.0.1:5000`.

---

### Step 4: Demonstration and Findings

Here we demonstrate how the generated payloads successfully evade the simple WAF.

#### Test 1: A Standard XSS Attack (Blocked)

Let's try a standard XSS payload.
**URL:** `http://127.0.0.1:5000/search?query=<script>alert('Blocked')</script>`

**Result:**
The page will display "Search Results for: alert('Blocked')/script". The WAF stripped out `<script>` and `<`. The attack fails.

#### Test 2: Using a Payload from our Generator (Success!)

Now, let's run `payload_generator.py`. One of the generated payloads will be:
```html
<svg/onload=alert('XSS')>
```
This payload uses an `<svg>` tag and an `onload` event, neither of which our simple WAF is configured to block.

**URL:** `http://127.0.0.1:5000/search?query=<svg/onload=alert('XSS')>`

**Result:**
An alert box with the message "XSS" will pop up in your browser.



**Why it Worked:**
The attack was successful because the WAF was only looking for a specific set of signatures. Our payload did not contain `<script>`, `onerror`, `<`, or `>`. It used `<svg/onload=...`, which flew under the WAF's radar but was still executed by the browser as valid HTML/JavaScript.

#### Conclusion

This exercise demonstrates a critical weakness of signature-based WAFs: they can only block what they know. A determined attacker can always find new ways to obfuscate payloads to bypass a static list of rules.

**Proper Mitigation:**
The real solution is not an endless race to update WAF blacklists. The best defense is:
1.  **Context-Aware Output Encoding:** On the server-side, encode any user-supplied data *before* rendering it in HTML. For example, convert `<` to `<`, `>` to `>`, and `"` to `"`. This neutralizes the payload, turning it into harmless text.
2.  **Content Security Policy (CSP):** A CSP header tells the browser which sources of content (like scripts) are legitimate. A strong CSP can prevent the execution of inline scripts altogether, making most XSS attacks impossible.
