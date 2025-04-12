from app import init_app
import os

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '1') == '1'
    host_addr = os.getenv('FLASK_HOST', '0.0.0.0')
    port_num = int(os.getenv('FLASK_PORT', 5000))

    app = init_app()

    print(f"🚀 Starting server on {host_addr}:{port_num} (debug={debug_mode})")
    app.run(debug=debug_mode, host=host_addr, port=port_num)
