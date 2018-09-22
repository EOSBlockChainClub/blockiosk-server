/**
  * @author sunny lee
  * @date 2018-09-23
  */
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosio.token/eosio.token.hpp>
#include <string>
using namespace eosio;

class blockiosk : public contract {
    private:
        /// @abi table accounts
        struct accounts {
            account_name    owner;
            eosio::asset    balance;

            uint64_t primary_key()const { return owner; }
        };

        /// @abi table actions
        struct actions {
            uint64_t        id;
            uint64_t        action_type;
            account_name    owner;
            std::string     where;
            std::string     memo;
            time            create_time;

            uint64_t primary_key()const { return id; }
        };

        void record_actions( uint64_t action_type, account_name owner, st::string where, std::string memo, time create_time){
            _accounts account(_self, _self);
            account.emplace( _self, [&]( auto& a ){
                a.id = account.available_primary_key();
                a.action_type = action_type;
                a.owner = owner;
                a.where = where;
                a.memo = memo;
                a.create_time = now();
            });
        }

    public:
        blockiosk( account_name self ):contract(self){}

        typedef eosio::multi_index<N(accounts), accounts> _accounts;
        typedef eosio::multi_index<N(actions), actions> _actions;

        void getbalance( account_name owner ) {
            _accounts account(_self, _self);

            auto acnt = account.get( owner );
            auto acnt_obj = name{acnt.owner};
            std::string acnt_str = acnt_obj.to_string();
            print(acnt_str, ": ", acnt.balance);
        }
};

EOSIO_ABI( blockiosk, (recordactions)(getbalance) )
