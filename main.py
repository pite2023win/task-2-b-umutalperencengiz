import multiprocessing
import random
import logging
import time



logging.basicConfig(level=logging.INFO)


class Car:

    def __init__(self, model, speed, wheelAngle, position, time):
        self.model = model
        self.speed = speed
        self.wheelAngle = wheelAngle
        self.position = position
        self.time = time

    def positionCalculator(self):
        self.position += self.speed * (self.wheelAngle / 360)

    def accelerate(self):
        self.speed += random.gauss(8, 10)

    def wheelMove(self):
        self.wheelAngle = random.gauss(90, 80)

    def timeCalculate(self):
        self.time += 1

    def simulation(self):
        self.positionCalculator()
        self.accelerate()
        self.wheelMove()
        self.timeCalculate()


class Environment:
    def __init__(self, weather, pedestrian, animal, car, redLight):
        self.weather = weather
        self.pedestrian = pedestrian
        self.animal = animal
        self.car = car
        self.redLight = redLight


class Event(Environment):

    def __init__(self, weather, pedestrian, animal, car, redLight):
        super().__init__(weather, pedestrian, animal, car, redLight)

    def combinedAc(self, other):
        if self.weather > 0.88 and self.pedestrian == 1:
            logging.info("!!! Car skidded and hit the pedestrian , pedestrian died !!!")
            self.weather = self.pedestrian = 0
        elif self.weather > 0.88 and self.pedestrian == 1 and self.animal > 0.97:
            logging.info("!!!The pedestrian and his dog died :(!!! ")
            self.weather = self.pedestrian = self.animal = 0
        elif (self.weather > 0.88 and self.car > 0.96) and (other.weather > 0.88 and other.car > 0.96):
            logging.info("!!! Cars skidded and crushed each other , drivers in intensive car unit !!!")
            self.weather = self.car = other.weather = other.car = 0

    def weatherAc(self):
        if self.weather > 0.88:
            if 0.88 < self.weather < 1:
                logging.info("!!! Car skidded because of the rain !!!")
            elif self.weather == 1:
                logging.info("!!! Car stuck in the snow!!!")

    def pedestrianAc(self):
        if self.pedestrian == 1:
            logging.info("!!! Car hit the pedestrian harsh, pedestrian died !!!")
        elif 0.95 < self.pedestrian < 1:
            logging.info("Car stopped about to hit the pedestrian,accident missed")

    def animalAc(self):
        if self.animal == 1:
            logging.info("!!! Poor animal died")
        elif 0.97 < self.animal < 1:
            logging.info("That was a nearby animal accident")

    def carAc(self, other):
        if 0.97 < self.car < 1 and 0.97 < other.car < 1:
            logging.info("!!! Cars crushed each other due to lack of attention !!!")
        if 0.90 < self.car < 0.97 and 0.90 < other.car < 0.97:
            logging.info("That was a nearby car accident between cars")

    def redAc(self):
        if self.redLight > 0.88:
            logging.info("!!! Passed in red probable accident !!!")
        else:
            pass

    def eventHandler(self, other):
        self.combinedAc(other)
        self.carAc(other)
        self.weatherAc()
        self.pedestrianAc()
        self.animalAc()
        self.redAc()


def simulate_car(cars):

    car1, car2 = cars

    while True:
        car1.simulation()
        car2.simulation()
        environment1 = Environment(random.gauss(0.5, 0.5), random.gauss(0.5, 0.5), random.gauss(0.5, 0.5),
                                       random.gauss(0.5, 0.5), random.gauss(0.5, 0.5))
        environment2 = Environment(random.gauss(0.5, 0.5), random.gauss(0.5, 0.5), random.gauss(0.5, 0.5),
                                       random.gauss(0.5, 0.5), random.gauss(0.5, 0.5))
        event1 = Event(
                environment1.weather, environment1.pedestrian, environment1.animal, environment1.car, environment1.redLight)
        event2 = Event(
                environment2.weather, environment2.pedestrian, environment2.animal, environment2.car, environment2.redLight)
        logging.info(f"{car1.model} - Position: {car1.position}, Speed: {car1.speed}")
        event1.eventHandler(event2)
        logging.info(f"{car2.model} - Position: {car2.position}, Speed: {car2.speed}")
        event2.eventHandler(event1)
        time.sleep(1)





def car_generator():
    while True:
        yield Car("Mustang", 70, 20, 0, 10), Car("Toyota", 80, 20, 0, 15)


if __name__ == "__main__":
    car_gen = car_generator()
    cars = next(car_gen)

    with multiprocessing.Pool(2) as pool:
        pool.map(simulate_car, [cars])
#You can exit with terminal exit key or exiting terminal or directly stop in IDE's I could not find exiting way with keyboardInterrupt or with any other way because of multiprocessing if you know how to exit in multiprocessing  pleasee share.




