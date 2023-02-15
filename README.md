# public-portfolio
portfolio i made public
This respository is a sub-repository of a larger project i'm working on in private
class Pancake take in 2 arguments only; token_contract, amount(the quantity of token)
example:
from pancake import pancakeswap_api

cake = pancakeswap_api(token_contract, amount)
cake.buy() #returns the swap rate if you are going to buy x amount of a token for usdt
cake.sell() #returns the swap rate if you are going to sell x amount of a token for usdt
cake.all() #returns both cake.buy() and cake.sell() as a dictionary containing both
cake.cal_uniswapize(no_of_turns, amount_diff)
      """
      cal_uniswapize can be used if you want rate of different amount of a token at once
      cal_uniswapize takes in 2 arguments:amount_diff(the number you would like to add to the main amount in the panckeswap_api arguments
                                          no_of_turn(number of times you want to add ammount_diff)
      cal_uniswapize returns a dictionary containing the swap rates for different amount
      i.e
      pancake = pancakeswap_api("0x0e349b8272b2E986436C8bd2B2B7944ae28d8778", 500)
      pancake.cal_uniswapize(5, 5) #if main amount is x, this returns the swap rate for 5+x, 5+5+x, 5+5+5+x, and so on.
      """
