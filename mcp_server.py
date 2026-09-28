"""MCP stdio server for FFT Engine."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import FastFourierTransform

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compute_fft",
                        "description": "Compute Fast Fourier Transform of real/complex signal vector (length power of 2)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "signal": {"type": "array", "items": {"type": "number"}}
                            },
                            "required": ["signal"]
                        }
                    },
                    {
                        "name": "compute_ifft",
                        "description": "Compute Inverse FFT from frequency spectrum components",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "real": {"type": "array", "items": {"type": "number"}},
                                "imag": {"type": "array", "items": {"type": "number"}}
                            },
                            "required": ["real", "imag"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "compute_fft":
            sig = args.get("signal", [])
            spectrum = FastFourierTransform.fft(sig)
            real = [round(c.real, 5) for c in spectrum]
            imag = [round(c.imag, 5) for c in spectrum]
            magnitudes = [round(abs(c), 5) for c in spectrum]
            return {"jsonrpc": "2.0", "id": req_id, "result": {"real": real, "imag": imag, "magnitudes": magnitudes}}
        elif name == "compute_ifft":
            r = args.get("real", [])
            im = args.get("imag", [])
            spec = [complex(a, b) for a, b in zip(r, im)]
            recon = FastFourierTransform.ifft(spec)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"signal": recon}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
