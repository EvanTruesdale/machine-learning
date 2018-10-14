import numpy
import os
import sys
import subprocess

if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python'] + sys.argv)

def Import_Data(filename):
   training_data_filename = filename
   with open(training_data_filename, "r") as file:
      n = len(file.readline().split("\t"))
   m = 0
   X = numpy.empty([0, n])
   Y = numpy.empty([0])
   with open(training_data_filename, "r") as file:
      for line in file:
         row = numpy.array([1])
         temp_list = list(map(float, line.rstrip().split("\t")))
         Y = numpy.append(Y, temp_list[n-1:])
         row = numpy.append(row, temp_list[0:-1])
         X = numpy.append(X, [row], axis = 0)
         m += 1

   mean = numpy.empty([0])
   stdev = numpy.empty([0])
   for i in range(0, n):
      mean = numpy.append(mean, X[:,i].mean())
      stdev = numpy.append(stdev, X[:,i].std())
      if(stdev[i] != 0):
         X[:,i] = [value - mean[i] for value in X[:,i]] / stdev[i]
   return m, n, X, Y, mean, stdev

def dJ(theta, m, n, X, Y):
   steps = numpy.empty([0])
   for j in range(0, n):
      sum = 0
      for i in range(0, m):
         difference = numpy.sum(numpy.multiply(X[i, 0:], theta)) - Y[i]
         sum += difference * X[i, j]
      steps = numpy.append(steps, sum / m)
   return steps

m, n, X, Y, mean, stdev = Import_Data("training_data.txt")
theta = numpy.zeros(n)
alpha = 0.3
print(theta)
while True:
   last_theta = theta
   temp_array = numpy.subtract(theta, alpha * dJ(theta, m, n, X, Y))
   theta = temp_array
   print(theta)
   stop = True
   for i in range(0, n):
      if abs((theta[i] - last_theta[i])/theta[i]) < .001:
         fakeCode=stop
      else:
         stop = False
      if(numpy.isnan(theta[i])):
         print("Alpha is too large")
         break
   if stop:
      print("Thetas")
      print(theta)
      print("Means")
      print(mean)
      print("Stdevs")
      print(stdev)
      print("Writing Thetas to File...")

      with open("theta_data.txt", "w") as output:
          for number in theta:
              output.write(str(number)+"\n")
      print("Writing Done")
      break
