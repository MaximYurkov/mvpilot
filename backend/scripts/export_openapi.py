import json
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))

from app.main import app


output_path = backend_path / 'openapi.json'
output_path.write_text(
    json.dumps(app.openapi(), ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'OpenAPI specification saved to {output_path}')
