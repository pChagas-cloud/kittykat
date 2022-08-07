#!/usr/bin/env python

import os
import click

default_todolist_file = os.path.join(os.path.expanduser('~'), '.config', 'kittykat', 'tasklist')
default_idealist_file = os.path.join(os.path.expanduser('~'), '.config', 'kittykat', 'idealist')
 

class program_backend:
    def __init__(self):
        self.idealistPath = default_idealist_file
        self.tasklistPath = default_todolist_file
        f = open(self.tasklistPath, 'r')
        tasklist = []
        for i in f.readlines():
            tasklist.append(i)
        f.close()
        self.tasklist = tasklist

    # BEGIN OF FILE-PROCESSING

    # Creates a vector that contains all the tasks packages
    # A task package is an tuple with the task string, and a bool (0 or 1) that must inform if the task is completed or not (0=not completed, 1=completed)
    def get_tasks_data(self):
        tasks = []
        dones = []
        counter = 0
        for i in self.tasklist:
            if counter == 0:
                tasks.append(i)
                counter += 1
            else:
                dones.append(i)
                counter -= 1
        aio = []
        for i in range(len(tasks)):
            package = (tasks[i].strip(), dones[i].strip())
            aio.append(package)
        return aio

    # Returns the tasklist length (tasklist = return of get_tasks_data, which returns the touples)
    def return_taskfile_len(self):
        length = len(self.get_tasks_data())
        return length

    # Takes the vector returned by get_tasks_data, reads it, and returns an vector with the string ready to print
    # PRINT THIS, FRONT END
    def task_data_to_string(self):
        taskdata = self.get_tasks_data()
        tasks_string = []
        for i in taskdata:
            if i[1] == 1 or i[1] == "1":
                task_string = f"{i[0]} [X]"
            else:
                task_string = f"{i[0]} [ ]"
            tasks_string.append(task_string)
        return tasks_string

    # END OF FILE-PROCESSING

    # BEGIN OF FILE-WRITING

    # This function takes a touple that contais the task string, and the completed? bool and writes it on the "tasklist" file
    def write_new_task(self, tasktuple):
        task = tasktuple[0]
        done = tasktuple[1]
        task = f'{task}\n'
        done = f'{done}\n'
        new_content = []
        new_content.append(task)
        new_content.append(done)
        tasklist_new_file = open(self.tasklistPath, 'a')
        for i in new_content:
            tasklist_new_file.writelines(i)
        tasklist_new_file.close()

    # This function takes a task_index, and removes from the output of get_tasks_data the touple [task string + complete? bool] that corresponds to that index
    # After that, it errases the tasklist file from the self.tasklistPath and writes the elements on the new get_tasks_data vector/array
    def delete_task(self, taskindex):
        taskindex = int(taskindex)
        taskindex = taskindex-1
        taskdata = self.get_tasks_data()
        deleted_task = taskdata[taskindex]
        taskdata.pop(taskindex)
        open(self.tasklistPath, 'w').close()
        f = open(self.tasklistPath, 'a')
        for i in taskdata:
            for k in i:
                f.writelines(f'{k}\n')
        f.close()
        return deleted_task

    # This function simply rewrites a bool variable on the self.tasklistPath file, changing from 0 to 1 or from 1 to 0.
    # Just in case you forgot, the 0 represents that the task is NOT COMPLETED, and 1 represents that the task is COMPLETED
    def mark_as_done(self, task_index):
        taskindex = int(task_index)
        if taskindex == 0:
            taskindex = 1
        else:
            taskindex = taskindex * 2 - 1
        f = open(self.tasklistPath, 'r')
        old_task_data = f.readlines()
        f.close()
        if old_task_data[taskindex].strip() == '0':
            old_task_data[taskindex] = '1\n'
            task_status = 'done'
        else:
            old_task_data[taskindex] = '0\n'
            task_status = 'not done'
        open(self.tasklistPath, 'w').close()
        with open(self.tasklistPath, 'a') as f:
            for i in old_task_data:
                f.writelines(i)
        return (task_status, old_task_data[taskindex-1])
        
    # This function takes the task_data_to_string returned values and print them on the screen
    def print_tasks(self):
        tasks = self.task_data_to_string()
        for i in range(len(tasks)):
            print(f'{i+1} - {tasks[i]}')

    # This function is quite bloated, but it does the job. It takes an task index and changes it to a new task that the user can type
    # It's 6AM and I am sleepy. Sorry for the terrible comment
    def edit_task(self, task_index):
        taskindex = int(task_index)
        taskindex -= 1
        tasklist = self.get_tasks_data()
        print(tasklist)
        print(f'kittykat: you are editing: {tasklist[taskindex][0]}') 
        new_task = input('kittykat: Type the new task! \n:')
        done = input('kittykat: Great! Now, is it done? [Y/n] ')
        while done.strip().lower() != "yes" and done.strip().lower() != "y" and done.strip().lower() != "no" and done.strip().lower() != "n":
            print('kittykat: Please, enter a valid "Y/N" answer...')
            done = input(":")
        if done == 'y' or done == 'yes':
            tasklist[taskindex] = (new_task, '1')
        else:
            tasklist[taskindex] = (new_task, '0')
        open(self.tasklistPath, 'w').close()
        with open(self.tasklistPath, 'a') as f:
            for i in tasklist:
                for k in i:
                    f.writelines(f'{k}\n')
        print(f'kittykat: modified task {task_index}, that now is: "{new_task}"')


    #----------- START MESSING WITH IDEAS ---------------#

    # This function read the self.idealistPath file (that contais the ideas and it's descriptions) and returns a vector that contains: [ (idea1, idea1_desc), (idea2, idea2_desc)...]
    def get_idea_package(self):
        ideas = []
        descriptions = []
        with open(self.idealistPath, 'r') as f:
            counter = 0
            for i in f.readlines():
                if counter == 0:
                    ideas.append(i)
                    counter += 1
                else:
                    descriptions.append(i)
                    counter -= 1
        package = []
        for i in range(len(ideas)):
            pack = (ideas[i], descriptions[i])
            package.append(pack)
        return package

    def get_ideafile_len(self):
        return len(self.get_idea_package())

    # This function gets the package returned by get_idea_package and prints the ideas, with or without descriptions (1=with_desc, 2=without_desc)
    def print_ideas(self, print_desk):
        idea_list = self.get_idea_package()
        if print_desk == 1:
            for i in range(len(idea_list)):
                print(f"{i+1} - {idea_list[i][0].strip()}")
                print(f"    description: {idea_list[i][1].strip()}")
        else:
            for i in range(len(idea_list)):
                print(f"{i+1} - {idea_list[i][0].strip()}")

    # This function takes a new idea from the user, asks for a desc, and then writes it on the self.idealistPath
    def add_idea(self, idea):
        current_ideas = self.get_idea_package()
        print('kittykat: add idea description?')
        descbool = input('[Y/n]')
        while descbool.strip().lower() != "yes" and descbool.strip().lower() != "y" and descbool.strip().lower() != "no" and descbool.strip().lower() != "n":
                print('kittykat: Please, enter a valid "Y/N" answer...')
                descbool = input(":")
        if descbool == 'y' or descbool == 'yes':
            print('kittykat: Write the idea description here:')
            idea_desc = input(': ')
        else:
            idea_desc = 'This idea does not have a description!'
        new_idea = (f'{idea}\n', f'{idea_desc}\n')
        current_ideas.append(new_idea)
        open(self.idealistPath, 'w').close()
        with open(self.idealistPath, 'a') as f:
            for i in current_ideas:
                for k in i:
                    f.writelines(f'{k}')

    # This function takes an idea_index from the user and deletes the idea+idea_desc pacakge from the self.idealistPath file
    def delete_idea(self, idea_index):
        idea_index -= 1
        current_ideas = self.get_idea_package()
        deleted_idea = current_ideas[idea_index]
        current_ideas.pop(idea_index)
        open(self.idealistPath, 'w').close()
        with open(self.idealistPath, 'a') as f:
            for i in current_ideas:
                for k in i:
                    f.writelines(k)
        return deleted_idea

    # This function takes an idea_index, gets a new idea from the user, and rewrites the idea relative to the idea_index on the self.idealistPath file
    def edit_idea(self, idea_index):
        idea_index -= 1
        current_ideas = self.get_idea_package()
        print(f'kittykat: You are editing: "{current_ideas[idea_index][0].strip()}"')
        new_idea = input('Kittykat: You can now rewrite the idea :) \n:')
        print('kittykat: add idea description?')
        descbool = input('[Y/n]')
        while descbool.strip().lower() != "yes" and descbool.strip().lower() != "y" and descbool.strip().lower() != "no" and descbool.strip().lower() != "n":
                print('kittykat: Please, enter a valid "Y/N" answer...')
                descbool = input(":")
        if descbool.strip().lower() == 'y' or descbool.strip().lower() == 'yes':
            print('kittykat: Write the idea description here:')
            idea_desc = input(': ')
        else:
            idea_desc = 'This task does not have a description!'
        new_idea_pack = (f'{new_idea}\n', f'{idea_desc}\n')
        current_ideas[idea_index] = new_idea_pack
        open(self.idealistPath, 'w').close()
        with open(self.idealistPath, 'a') as f:
            for i in current_ideas:
                for k in i:
                    f.writelines(k)


    # END OF FILE-WRITING

    def test_stuff(self):
        self.print_tasks()

@click.group
def cli():
    pass

@cli.group
def task():
    pass

@cli.group
def idea():
    pass

@task.command()
def list():
    if program_backend().return_taskfile_len() > 0:
        program_backend().print_tasks()
    else:
        print('kittykat: There are no tasks! Add one with "kittykat task add"')
@task.command()
@click.argument('index', type=int, required=1)
def delete(index):
    if int(index) <= 0:
        print('Kittykat: Hey, this index is clearly not valid >:(')
    else:
        if program_backend().return_taskfile_len() == 0:
            print('kittykat: There are no tasks! Add one with "kittykat task add"')
        else:
            if int(index) > program_backend().return_taskfile_len():
                print('kittykat: You dont have that many tasks, use "kittykat task list" to see your current tasks!') 
            else:
                delted_task = program_backend().delete_task(index)
                print(f'kittykat: Task: "{delted_task[0]}" deleted')

@task.command()
@click.argument('task')
def add(task):
    program_backend().write_new_task((task,0))
    print(f'kittykat: New task "{task}" added to tasklist!')

@task.command()
@click.argument('index', type=int, required=1)
def done(index):
    if int(index) <= 0:
        print('Kittykat: Hey, this index is clearly not valid >:(')
    else:
        if int(index) > program_backend().return_taskfile_len():
            print('kittykat: You dont have that many tasks, use "kittykat task list" to see your current tasks!') 
        else:
            completed_task = program_backend().mark_as_done(index)
            if completed_task[0].strip() == 'done':
                print(f'kittykat: Congratulations on completing "{completed_task[1].strip()}"!')
            else:
                print('kittykat: Well, more things to do then!')

@task.command()
@click.argument('index', type=int, required=1)
def edit(index):
    if int(index) <= 0:
        print('Kittykat: Hey, this index is clearly not valid >:(')
    else:
        if int(index) > program_backend().return_taskfile_len():
            print('kittykat: You dont have that many tasks, use "kittykat task list" to see your current tasks!') 
        else:
            program_backend().edit_task(index)
@idea.command()
@click.option('--showdesc', default=True, help='boolean value (1 or 0) that decides if the ideas description will be printed', type=bool)
def list(showdesc):
    if program_backend().get_ideafile_len() > 0:
        program_backend().print_ideas(showdesc)
    else:
        print('kittykat: There are no ideas! Add one with "kittykat idea add"')

@idea.command()
@click.argument('index', type=int, required=1)
def delete(index):
    if int(index) <= 0:
        print('Kittykat: Hey, this index is clearly not valid >:(')
    else:
        if program_backend().get_ideafile_len() == 0:
            print('kittykat: There are no ideas! Add one with "kittykat idea add"')
        else:
            if int(index) > program_backend().get_ideafile_len():
                print('kittykat: You dont have that many ideas, use "kittykat idea list" to see your current tasks!') 
            else:
                delted_idea = program_backend().delete_idea(index)
                print(f'kittykat: idea: "{delted_idea[0].strip()}" deleted')

@idea.command()
@click.argument('idea')
def add(idea):
    program_backend().add_idea(idea)
    print(f'kittykat: New idea "{idea}" added to idealist!')

@idea.command()
@click.argument('index', type=int, required=1)
def edit(index):
    if int(index) <= 0:
        print('Kittykat: Hey, this index is clearly not valid >:(')
    else:
        if int(index) > program_backend().get_ideafile_len():
            print('kittykat: You dont have that many ideas, use "kittykat idea list" to see your current ideas!') 
        else:
            program_backend().edit_idea(index)

if __name__ == "__main__":
    cli()
