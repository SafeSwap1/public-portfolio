
from web3 import Web3
from web3.middleware import geth_poa_middleware
import sys, time
from functions import parallel


class pancakeswap_api:

    def __init__(self, token_contract, amount):
        w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.router_contract = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
        with open("pancake_router_abi.txt", "r") as file:
            self.abi = file.read()
        self.token_contract = token_contract
        self.amount = amount
        self.wbnb = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
        self.usdt = "0x55d398326f99059fF775485246999027B3197955"
        self.contract = w3.eth.contract(self.router_contract, abi=self.abi)
        
    def buy(self, new_amount = None):
        if new_amount == None:
            new_amount = self.amount
        *_, usdt_to_wbnb = self.contract.functions.getAmountsOut(new_amount*(10**18), [self.usdt, self.wbnb]).call()
        *_, wbnb_to_token = self.contract.functions.getAmountsOut(usdt_to_wbnb, [self.wbnb, self.token_contract]).call()
        swap_rate = new_amount/(wbnb_to_token/10**18)
        return {"buy": swap_rate}
    
    def sell(self, new_amount = None):
        if new_amount == None:
            new_amount = self.amount
        usdt_to_wbnb, *_ = self.contract.functions.getAmountsIn(new_amount*(10**18), [self.wbnb, self.usdt]).call()
        wbnb_to_token, first = self.contract.functions.getAmountsIn(usdt_to_wbnb, [self.token_contract, self.wbnb]).call()
        swap_rate = new_amount/(wbnb_to_token/10**18)
        return {"sell": swap_rate}
    
    def all(self, amount = None):
        if amount == None:
            amount = self.amount
        func = [(self.buy, amount), (self.sell, amount)]
        "return {self.amount: {'buy': self.buy(), 'sell': self.sell()}}"
        try:
            return {amount: {key: value for each in parallel(self.add_token, func) for key, value in each.items()}}
        except (ValueError) as e:
            print(e)
    
    def add_token(self, function, params):
        function = function(params)
        return function 
    
    def cal_uniswapize(self, no_of_turns: int, amount_diff: int):    
        lists = []
        no_of_turns = no_of_turns
        for _ in range(no_of_turns):
            lists.append(self.amount)
            self.amount+=amount_diff
        list_of_data = parallel(self.all, lists)

        dict_of_data = {key: value for each in list_of_data for key, value in each.items()}
        return ({key: dict_of_data[key] for key in sorted(dict_of_data)})     
    

def main():
    st = time.time()
    pancake = pancakeswap_api("0x0e349b8272b2E986436C8bd2B2B7944ae28d8778", 500)
    print(pancake.cal_uniswapize(20, 5))
    print(time.time() - st)

if __name__ == "__main__":
    main()