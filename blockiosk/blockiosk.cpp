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
        /// @abi table actions
        struct actions {
            account_name    owner;
            std::string     act_type;
            std::string     where;
            std::string     memo;
            time            create_time;

            uint64_t primary_key()const { return owner; }
        };


    public:
        blockiosk( account_name self ):contract(self){}
        typedef eosio::multi_index<N(actions), actions> _actions;

        void takeaction( account_name owner, std::string act_type, std::string where, std::string memo){
            _actions action(_self, _self);
            action.emplace( _self, [&]( auto& a ){
                a.act_type = act_type;
                a.owner = owner;
                a.act_type = act_type;
                a.where = where;
                a.memo = memo;
                a.create_time = now();
            });
        }

        void getaction( account_name owner ) {
            _actions action(_self, _self);

            auto act = action.get( owner );
            auto act_obj = name{act.owner};
            std::string act_str = act_obj.to_string();
            print(act_str, ": ", act.act_type, act.where, act.memo, act.create_time);
        }
};

EOSIO_ABI( blockiosk, (takeaction)(getaction) )
