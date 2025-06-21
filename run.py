from zapvault import create_app

app = create_app()
# DEBUG: List all routes
print("\n✅ Registered Flask Routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run(debug=True)
