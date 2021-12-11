import argparse
import json
from xml.dom.expatbuilder import parseString
import dicttoxml


def main():
    parser = argparse.ArgumentParser("Students, rooms, format")
    parser.add_argument("students", type=str, help="way for file students")
    parser.add_argument("rooms", type=str, help="way for file rooms")
    parser.add_argument("format", type=str, help="output format")
    args = parser.parse_args()

    with open(f"{args.rooms}", "r") as rooms:
        rooms = json.load(rooms)

    with open(f"{args.students}", "r") as students:
        students = json.load(students)
    rooms_dict = {}
    for room in rooms:
        room["students_list"] = []
        rooms_dict[room['id']] = room
    for student in students:
        rooms_dict[student['room']]['students_list'].append(f"{student['id']} -  {student['name']}")
    rooms = list(rooms_dict.values())
    writer = Writer.type_to_class[args.format.lower()]()
    writer.write_to_file(rooms)


class Writer:
    type_to_class = {}

    def write_to_file(self, data):
        pass

    @classmethod
    def writer_class(cls, format):
        def wrapper(wrapped):
            cls.type_to_class[format] = wrapped
            return wrapped

        return wrapper


@Writer.writer_class('xml')
class XMLWriter(Writer):
    def write_to_file(self, data):
        with open(f"result.xml", "w") as f:
            rooms_result = dicttoxml.dicttoxml(data, attr_type=False, custom_root="Rooms")
            rooms_result = parseString(rooms_result)
            rooms_result = rooms_result.toprettyxml(indent=" " * 4)
            f.write(rooms_result)


@Writer.writer_class('json')
class JSONWriter(Writer):
    def write_to_file(self, data):
        with open(f"result.json", "w") as f:
            json.dump(data, f, indent=3)


if __name__ == "__main__":
    main()
