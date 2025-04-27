from app import app 
from app.routes import rota1 , rota2
import os
from app.conexao import configurar_banco

if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))