# netbox_fastapi


## Webhook data models

### regions

```json
{
    event: 'created',
    timestamp: '2021-07-19 15:39:01.828640+00:00',
    model: 'region',
    username: 'admin',
    request_id: '3a66bcb7-dbb3-45d0-9f69-7e8d070935de',
    data: {
        id: 9,
        url: '/api/dcim/regions/9/',
        display: 'test',
        name: 'test',
        slug: 'test',
        parent: null,
        description: '',
        custom_fields: {},
        created: '2021-07-19',
        last_updated: '2021-07-19T15:39:01.813067Z',
        _depth: 0
    },
    snapshots: {
        prechange: null,
        postchange: {
            created: '2021-07-19',
            last_updated: '2021-07-19T15:39:01.813Z',
            parent: null,
            name: 'test',
            slug: 'test',
            description: '',
            custom_fields: {}
        }
    }
}
```