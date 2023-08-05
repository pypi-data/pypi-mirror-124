# mkdocs-github-contributors-plugin

Plugin for [MkDocs](https://mkdocs.org). Inserts a list of GitHub contributors.

```yaml
plugins:
  - github-contributors:
      repository: <repo>

      # optional
      clientId: <clientId>
      clientSecret: <clientSecret>
```

## Options

- `repository`: should be in the form `${owner}/${repo}`
