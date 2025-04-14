# ChristianGirls

Your very own church of confessions

## Setup

1. **Clone the repo**

```bash
git clone <repo-url>
cd christiangirlssite
```

2. **Create a `.env` file**

Create a `.env` file in the root directory with the following variables:
(in this blog we are also fetching gifs from giphy so create a free giphy api key too <3)

```env
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///blog.db
GIPHY_API_KEY=your_giphy_api_key
```

3. **Set up a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Create the database**

```bash
python3
```

Then run:

```python
from christiangirls import LetThereBeLight, db
from christiangirls.models import User, Post

app = LetThereBeLight()
app.app_context().push()
db.create_all()
```

Start praying
