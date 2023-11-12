#!/usr/bin/python3
"""Defines the HBnB main console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_brackets = re.search(r"\{(.*?)\}", arg)
    parenthesis = re.search(r"\[(.*?)\]", arg)
    if curly_brackets is None:
        if parenthesis is None:
            return [i.strip(",") for i in split(arg)]
        else:
            regex = split(arg[:parenthesis.span()[0]])
            rtn_list = [i.strip(",") for i in regex]
            rtn_list.append(parenthesis.group())
            return rtn_list
    else:
        regex = split(arg[:curly_brackets.span()[0]])
        rtn_list = [i.strip(",") for i in regex]
        rtn_list.append(curly_brackets.group())
        return rtn_list


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def default(self, arg):
        """Default xtics for cmd module when input is invalid"""
        dict_args = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match_arg = re.search(r"\.", arg)
        if match_arg is not None:
            arg_len = [arg[:match_arg.span()[0]], arg[match_arg.span()[1]:]]
            match_arg = re.search(r"\((.*?)\)", arg_len[1])
            if match_arg is not None:
                command = [arg_len[1][:match_arg.span()[0]],
                           match_arg.group()[1:-1]]
                if command[0] in dict_args.keys():
                    call = "{} {}".format(arg_len[0], command[1])
                    return dict_args[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arg_len = parse(arg)
        if len(arg_len) == 0:
            print("** class name missing **")
        elif arg_len[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_len[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_len = parse(arg)
        dict_object = storage.all()
        if len(arg_len) == 0:
            print("** class name missing **")
        elif arg_len[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_len) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_len[0], arg_len[1]) not in dict_object:
            print("** no instance found **")
        else:
            print(dict_object["{}.{}".format(arg_len[0], arg_len[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_len = parse(arg)
        dict_object = storage.all()
        if len(arg_len) == 0:
            print("** class name missing **")
        elif arg_len[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_len) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_len[0], arg_len[1]) not in dict_object.keys():
            print("** no instance found **")
        else:
            del dict_object["{}.{}".format(arg_len[0], arg_len[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a class.
        If no class is specified, displays all instantiated objects."""
        arg_len = parse(arg)
        if len(arg_len) > 0 and arg_len[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg_len) > 0 and arg_len[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_len) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a class."""
        arg_len = parse(arg)
        counter = 0
        for obj in storage.all().values():
            if arg_len[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by creating or updating
        a given attribute key/value pair or dictionary."""
        arg_len = parse(arg)
        dict_object = storage.all()

        if len(arg_len) == 0:
            print("** class name missing **")
            return False
        if arg_len[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_len) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_len[0], arg_len[1]) not in dict_object.keys():
            print("** no instance found **")
            return False
        if len(arg_len) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_len) == 3:
            try:
                type(eval(arg_len[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_len) == 4:
            obj = dict_object["{}.{}".format(arg_len[0], arg_len[1])]
            if arg_len[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_len[2]])
                obj.__dict__[arg_len[2]] = val_type(arg_len[3])
            else:
                obj.__dict__[arg_len[2]] = arg_len[3]
        elif type(eval(arg_len[2])) == dict:
            obj = dict_object["{}.{}".format(arg_len[0], arg_len[1])]
            for key, val in eval(arg_len[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key])
                        in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(val)
                else:
                    obj.__dict__[key] = val
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
