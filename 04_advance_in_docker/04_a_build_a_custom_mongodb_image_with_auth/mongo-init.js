db.auth('admin-user', 'admin-password')

db = db.getSiblingDB('test-database')

db.createUser({
  user: 'test-user',
  pwd: 'test-password',
  roles: [
    {
      role: 'root',
      db: 'admin',
    },
  ],
});