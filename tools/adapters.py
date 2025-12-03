# tools/adapters.py
import logging
from typing import Any, Dict, List

log = logging.getLogger("tools")

class SpecComparator:
    def compare(self, specs: Dict[str, Any], observed: Dict[str, Any]) -> Dict[str, Any]:
        # Example comparison logic; expand to your domain needs
        result = {"flags": [], "matches": []}
        for k, v in specs.items():
            ov = observed.get(k)
            if ov is None:
                result["flags"].append(f"Missing observed value for {k}")
            elif ov == v:
                result["matches"].append(k)
            else:
                result["flags"].append(f"{k}: observed {ov} vs spec {v}")
        return result

# You can expose these to agents by precomputing context and injecting
# it into messages, or via a lightweight tool-calling protocol you define.
