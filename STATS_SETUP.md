# Self-hosting github-readme-stats (for the Stats + Top-Languages cards)

The public `github-readme-stats.vercel.app` is unreliable / currently paused.
Deploying your own copy takes ~3 minutes and is free. You do the account +
token steps (they involve credentials); then paste me the URL and I finish.

## 1. Create a GitHub token (for the stats backend to read your data)
1. Go to https://github.com/settings/tokens?type=beta  (fine-grained token)
2. **Generate new token** → name it `readme-stats`, expiration: 1 year
3. Resource owner: your account. Repository access: **Public repositories (read-only)** is enough.
4. Generate, then **copy the token** (starts with `github_pat_...`). Keep it handy for step 3.
   - (A classic token with **no scopes** also works if you prefer.)

## 2. Deploy github-readme-stats to Vercel
1. Go to https://github.com/anuraghazra/github-readme-stats
2. In its README, click the **“Deploy to Vercel”** button (or: fork the repo, then
   at https://vercel.com/new import your fork).
3. Sign in to Vercel **with GitHub** (free “Hobby” plan).
4. On the import/config screen, add an **Environment Variable**:
   - **Name:** `PAT_1`
   - **Value:** the token from step 1
5. Click **Deploy** and wait for it to finish.

## 3. Get your instance URL
After deploy, Vercel shows a domain like:
`https://github-readme-stats-xxxx.vercel.app`

Open `https://<your-domain>/api?username=Omai4x` to confirm a stats card renders.

## 4. Tell me the domain
Paste the base domain (e.g. `github-readme-stats-xxxx.vercel.app`) back to me and
I'll swap it into `README.md` (replacing `github-readme-stats.vercel.app`) and push.

Or do it yourself:
```
sed -i '' 's/github-readme-stats.vercel.app/YOUR-DOMAIN.vercel.app/g' README.md
git commit -am "Point stats cards at self-hosted instance" && git push
```

> Security note: never paste the token into chat or into the README — it only goes
> into Vercel's Environment Variables field. I never see or handle it.
