# Executing Locally via Intellij
To execute scripts locally on your machine you need to have ***Intellij***, ***PTG2***, and the entire ***RTP testing repository*** installed
on your machine before continuing with the instructions below. See our [Getting Started](..\getting-started.md) page on how to accomplish this.


#### Step 1 - Click "Edit Configurations..." option in the drop down on the toolbar.
![Step 1](/images/intellij-setup/python_execute_configurations/edit_configurations.png)

#### Step 2 - Add a new Python configuration.

![Step 2](/images/intellij-setup/python_execute_configurations/add_new_config.png)

#### Step 3 - Fill in fields.
* Name - name your configuration.
* Script - `[path to ISPFTest.py]` Path should be similar to: <br>

        C:\Users\spean03\IdeaProjects\RTP\rtppy\speantest\ISPFTest.py
        
* Script Parameters - Specify minimally the [--file](command-line-options.md#file) command line parameter and other needed RTPPY [Command Line Overrides](command-line-options.md) 
* Working Directory - `[path to rtppy directory in Intellij repository]` Path should be similiar to: <br>

        C:\Users\spean03\IdeaProjects\RTP\rtppy
    
![Step 2](/images/intellij-setup/python_execute_configurations/fill_in_fields.png)

#### Example
![Example](/images/intellij-setup/python_execute_configurations/example_configuration.png)

#### Step 5 - Run it
![Step 5](/images/intellij-setup/python_execute_configurations/run_configuration.png)