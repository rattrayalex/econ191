from random import gauss

from Person import t0_income_mu, t0_income_sigma


house_price_mu = t0_income_mu * 3
house_price_sigma = t0_income_sigma * 3


class House(object):

  def __init__(self, plot):
    self.price = gauss(house_price_mu, house_price_sigma)
    self.plot = plot
    self.owner = None
    self.occupant = None

  def __str__(self):
    owner_name = self.owner.name if self.owner else None
    occupant_name = self.occupant.name if self.occupant else None
    return "H<owner:{}, occupant:{}, price:{}>".format(
      owner_name, occupant_name, int(self.price))

  def rent(self):
    return self.price / 10

  def is_for_sale(self):
    return self.owner is None

  def buy(self, owner):
    if not self.is_for_sale():
      raise Exception('Not for Sale!')
    self.owner = owner
    return self

  def is_unoccupied(self):
    return self.occupant is None

  def occupy(self, occupant):
    if not self.is_unoccupied():
      raise Exception('Someone lives here already!')
    self.occupant = occupant
    return self


