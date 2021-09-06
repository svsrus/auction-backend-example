create database scopic_auction_test;
create user scopic_auction_test_user;
alter role scopic_auction_test_user with password 'test123456';
grant all privileges on database scopic_auction_test to scopic_auction_test_user;
alter user scopic_auction_test_user createdb;
alter database scopic_auction_test owner to scopic_auction_test_user;
