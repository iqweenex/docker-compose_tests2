from tests.utils.logger import Logger


class TestGradesStatsE2E:

    def test_full_stats_scenario(self, university_service, generator):
        Logger.info("Start e2e test")

        group = university_service.create_group(generator.group())
        teacher = university_service.create_teacher(generator.teacher())
        student1 = university_service.create_student(generator.student(group_id=group.id))
        student2 = university_service.create_student(generator.student(group_id=group.id))

        stats_before = university_service.get_stats()
        Logger.info(f"Stats до: count={stats_before.count}")

        grades_per_student = 2
        students = [student1, student2]
        total_grades_created = len(students) * grades_per_student

        for student in students:
            for _ in range(grades_per_student):
                university_service.create_grade(
                    generator.grade(student_id=student.id, teacher_id=teacher.id)
                )

        stats_after = university_service.get_stats()
        Logger.info(f"Stats после: count={stats_after.count}")
        assert stats_after.count == stats_before.count + total_grades_created

        all_grades = university_service.get_grades()
        grades_to_delete = [g for g in all_grades if g.student_id == student1.id]

        for grade in grades_to_delete:
            Logger.info(f"Удаляем оценку {grade.id}")
            university_service.delete_grade(grade.id)

        university_service.delete_student(student1.id)

        stats_final = university_service.get_stats()
        Logger.info(f"Stats итог: count={stats_final.count}")
        assert stats_final.count == stats_after.count - len(grades_to_delete)
        assert hasattr(stats_final, "min")
        assert hasattr(stats_final, "max")
        assert hasattr(stats_final, "avg")
