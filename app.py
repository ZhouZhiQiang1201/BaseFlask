# -*- config: utf-8 -*-
print("celery")
from myapp import create_app, celery


app = create_app()


if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=8989)