# Seismic Events Analysis STA/LTA algorithm
This project contains scripts for analyzing seismic signals using Apollo data and `.mseed` files.


## Instructions for use
1. Clone the repository.
2. Make sure that the following dependencies are installed:
   - numpy
   - pandas
   - obspy
   - matplotlib
   - datetime
   - scipy
   - google-generativeai
   - noisereduce
   - python-dotenv
   - fastapi
   - uvicorn
   - python-multipart
3. Organize the data in the `/data` folder.
4. Run the analysis from the notebook or the Python scripts. 

## Execution
Open the notebook at `/notebooks/v1_notebook.ipynb` to see detailed steps on how to process the signal data.


## Algorithm v2

Version 2 of the algorithm introduces several key improvements for seismic event detection, which optimize both the performance and accuracy of the analysis:

1. **Event Filtering Optimization**:
   - Detected events are now more precisely filtered and merged to avoid the detection of spurious events or false positives.
   - Conditions have been added to avoid merging unrelated events and improve signal analysis.

2. **Improved Management of Detected Events**:
   - The code has been restructured to perform a more efficient traversal of detected events. Now, detection is faster and more accurate, with better handling of the start and end times of each event.

3. **Enhanced Visualization**:
   - The graphical display of events has been optimized to be clearer and easier to interpret. Detection areas are now highlighted more precisely, and labels are displayed with the exact start and end times of events.

4. **Detailed Event Reporting**:
   - Reporting of detected events includes improved numerical precision for detection times, providing more accurate results in signal analysis.

### How to use version 2

1. Run the `v2_notebook.ipynb` notebook to process the signals and view the detected events with the new enhancements.
2. Ensure to follow the project structure to load the data correctly and visualize the results with the new optimizations.


# Algorithm v3

Version 3 of the algorithm includes several key improvements, increasing the ability to detect multiple events in a single signal and further refining the seismic event detection process.

1. **Multiple Event Detection**:
   - The algorithm can now handle multiple events in a single run, with more refined logic that allows the detection and reporting of  multiple events in long signals.
   - The detection threshold was adjusted to avoid false positives and improve accuracy.

2. **Enhanced Visualization**:
   - Improvements were added to the generated graphs, better highlighting detected events and providing detailed labels for the start and end times of each event.
   - The STA/LTA characteristic function is displayed alongside the detections for more comprehensive analysis.

3. **Detailed Event Reporting**:
   - The code now reports each detected event in a detailed format, accurately showing the start and end times of each event in seconds.

### How to use version 3

1. Run the `v3_notebook.ipynb` notebook to analyze the signals and detect multiple events with the new enhancements.
2. Ensure to load the data correctly in the `/data` folder and verify the generated visualizations.


# Algorithm v4 

Version 4 introduces several key improvements to make seismic event detection more accurate and stable, regardless of variations in signal amplitudes.

1. **Signal Normalization**:
   - The algorithm now standardizes signal traces before analyzing them, ensuring that detected events are not affected by differences in signal amplitude.

2. **Optimization of the Event Fusion Process**:
   - A new parameter called `min_gap` has been implemented, which defines the minimum time interval between two events to merge them. This improves accuracy by avoiding merging events that are not closely related in time.

3. **Enhanced Display with Normalized Signals**:
   - Graphs now use normalized signals, enhancing the clarity of detected events. This makes interpretation of results more accurate and consistent.

4. **STA/LTA Threshold Control**:
   - Threshold control for event detection has been fine-tuned, allowing for more accurate and reliable detection.

### How to use version 4

1. Run the `v4_notebook.ipynb` notebook to process the normalized signals and detect events with the new fusion and threshold controls.
2. Ensure that your data is in the correct format and run the analysis in the `/data` folder to view the updated results.


# Algorithm v5

Version 5 of the algorithm introduces a major improvement in the evaluation of the accuracy of detections by calculating the absolute error between detected events and the true times of known events.

1. **Absolute Error Calculation**:
   - The code now computes the absolute error between the true time of the event and the detected time, which allows measuring the accuracy of the detection algorithm.
   
2. **Average Absolute Error**:
   - The calculation of the average absolute error for all detections has been added, providing an overall performance metric for the algorithm.

3. **Enhanced Detection Report**:
   - The detection report now includes both the detected time and the absolute error in seconds, offering a detailed analysis of the algorithm's performance on each event.

4. **Error Correction**:
   - Ensure to properly initialize the `merged_on_off` variable before using it to avoid execution errors.

### How to use version 5

1. Run the `v5_notebook.ipynb` notebook to analyze the seismic events and calculate the absolute and average errors in the detections.
2. Review the generated results to compare the accuracy of the algorithm with the true times of known events.


# Algorithm v6

Version 6 algorithm introduces the ability to generate graphs and save them in image format, as well as an interactive interface for labeling and saving detected signals.

1. **Generating and Saving Graphs**:
   - The algorithm now generates graphs of the detected signals and saves them as `.png` files. A name or number can be entered to label each graph when saving, facilitating the identification of the evidence.

2. **Interactive Interface**:
   - An interactive function (`input()`) has been added that allows the user to manually enter the name or number of the evidence before the plot of each signal is saved. This provides greater flexibility in handling different events.

3. **Detailed Signal Visualization**:
   - Each detected event generates a graph with a title indicating the signal number, and the start and end times of each detected event are displayed. This helps to clearly visualize the relevant signal segments.

4. **Report of Detected Events**:
   - The code continues to display the start and end times of detected events, using the format already established in previous versions.

### How to use version 6

1. Run the `v6_notebook.ipynb` notebook to process the seismic events.
2. When the algorithm detects a signal, a graph will be generated and you will be prompted to enter a name or number to save the image file.
3. Review the generated graphs to analyze the detected events and compare them visually.

# Algorithm v7

Version 7 of the algorithm introduces a more efficient visualization of the detected events and simplifies the graph generation flow.

1. **Enhanced Signal Visualization**:
   - Each detected signal is automatically visualized by a detailed graph, showing the start and end times of each event.

2. **Automatic Graph Generation**:
   - Graphs are automatically generated and displayed for each detected event. Unlike previous versions, the user is not prompted to enter a file name, making the process more straightforward.

3. **Simplification of the Display Process**:
   - User interaction has been eliminated, and graphs are generated automatically without the need to save image files.

4. **Reporting of Detected Events**:
   - The code continues to display the start and end times of each detected event in the console.

### How to use version 7

1. Run the `v7_notebook.ipynb` notebook to process the seismic events and automatically display the plots of the detected events.
2. Review the generated plots to analyze the detected events and the times of the relevant events.



# Algorithm v8 (final)

Version 8 of the algorithm implements **GEMINI**, a significant improvement for the detection and analysis of seismic events, focused on the validation and filtering of events according to minimum duration criteria.

1. **GEMINI** implementation:
   - GEMINI is used to detect seismic events more accurately, ensuring that only events that meet predefined criteria are considered valid.

2. **Filtering by Minimum Duration**:
   - Detected events are automatically filtered according to their minimum duration, eliminating those that do not meet the requirements.

3. **Enhanced Visualization**:
   - Detected events are clearly displayed in graphs, with vertical lines indicating trigger on and trigger off points on the seismogram.

4. **Detailed Event Reporting**:
   - The code reports in the console the valid events, showing start and end times in seconds.

### How to use version 8

1. Run the `v8_notebook.ipynb` notebook to process seismic events using GEMINI.
2. Detected events will be automatically displayed in graphs with on and off indicators.
3. Valid event times will be displayed in the console for detailed analysis.