from zapvault import create_app
import os

app = create_app()

# DEBUG: List all routes
print("\n✅ Registered Flask Routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

