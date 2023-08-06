# Computational Stopwatch

Simple stopwatch to easily print the elapsed time of a set of operations. It's a minimalistic library, but it is very useful in many real cases.

## Usage
The easiest way to use this tool is in conjunction with the **with** python statement.
```python
>> from computational_stopwatch import Stopwatch
>>
>> with Stopwatch():
>>  time.sleep(3) # <- simulates a long computation 
Elapsed time 0:00:03.003106
```
anything within the scope of the **with** statement will count against the elapsed time. An optional task name to be printed along the elapsed time (e.g. for better identification in a log) can be set in the constructor.

Alternatively, the class can be directly instantiated and the print function explicitly called.
```python
>> sw = Stopwatch()
>> time.sleep(3)
>> sw.print_elapsed_time()
Elapsed time 0:00:03.003280
```
The start time can be reset with the **reset_time** function and the **get_elapsed_time** method returns the unformatted elapsed time, which is useful for numerical comparisons.
