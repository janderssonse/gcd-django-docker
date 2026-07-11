-- Allow the app user to create and use the test databases that
-- pytest-django needs (test_my-gcd-db and similar).
GRANT ALL PRIVILEGES ON `test\_%`.* TO 'gcd-django'@'%';
FLUSH PRIVILEGES;
