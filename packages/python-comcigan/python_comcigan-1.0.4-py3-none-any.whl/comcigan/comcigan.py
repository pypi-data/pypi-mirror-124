from __future__ import annotations
from base64 import b64encode
from json import loads
from typing import Literal, Union
from urllib.request import urlopen
from re import search, sub
from bs4 import BeautifulSoup

class Comcigan:
	__URL: str = 'http://comci.kr:4082'
	__basePath: str = None
	__timetablePath: str = None
	__timetableObject: dict = None
	__subjectId: str = None
	__teacherId: str = None

	def __getRegexResult(self: Comcigan, string: str, regex: str) -> str:
		matchObject = search(pattern=regex, string=string)

		if(matchObject != None):
			return string[matchObject.start():matchObject.end()]
		else:
			return ''

	def __getResponseString(self: Comcigan, uri: str, encoding: Literal['UTF-8', 'EUC-KR']) -> str:
		string = b''.join(urlopen(uri).readlines()).decode(encoding)

		if(self.__getRegexResult(encoding, r'^[uU][tT][fF]-?8$') == None):
			return string
		else:
			return string.replace('\0', '')

	def __getTrimmedArray(self: Comcigan, array: list) -> list:
		lastZeroIndex = len(array)

		for i in range(len(array) - 1, -1, -1):
			if(array[i] == 0 or array[i] == ''):
				lastZeroIndex -= 1
			else:
				break

		if(lastZeroIndex == 0):
			return []
		else:
			return array[0:lastZeroIndex]

	def __init__(self: Comcigan, schoolName: str, schoolRegion: str) -> None:
		baseScript: str = BeautifulSoup(self.__getResponseString('http://comci.kr:4082/st', 'EUC-KR'), 'html.parser').find_all('script')[1].contents[0]
		self.__subjectId = self.__getRegexResult(baseScript, r'(?<=자료\.자료)\d+(?=\[sb\])')
		self.__teacherId = self.__getRegexResult(baseScript, r'(?<=성명=자료\.자료)\d+')
		self.__timetableId = self.__getRegexResult(baseScript, r'(?<=일일자료=자료\.자료)\d+')

		if(self.__subjectId == None):
			raise Exception('Invalid self.__subjectId regular expression in module')
		elif(self.__teacherId == None):
			raise Exception('Invalid self.__teacherId regular expression in module')
		elif(self.__timetableId == None):
			raise Exception('Invalid self.__timetableId regular expression in module')
		else:
			route: str = self.__getRegexResult(baseScript, r'\.\/\d+\?\d+l')

			if(route != None):
				self.__basePath = route[1:8]
				schools: list[int, str, str, int] = loads(self.__getResponseString(self.__URL + self.__basePath + route[8:] + str(schoolName.encode('EUC-KR')).upper()[2:-1].replace('\\X', '%'), 'UTF-8'))['학교검색']

				if(len(schools) != 0):
					for school in schools:
						if(school[1] == schoolRegion):
							self.__timetablePath = '?' + b64encode((self.__getRegexResult(baseScript, r'\'\d+_\'')[1:-1] + str(school[3]) + '_0_1').encode('UTF-8')).decode('UTF-8')

					if(self.__timetablePath != None):
						return None
					else:
						raise Exception('Invalid schoolRegion in parameter')
				else:
					raise Exception('Invalid schoolName in parameter')
			else:
				raise Exception('Invalid route regular expression in module')

	def synchronize(self: Comcigan) -> Comcigan:
		if(self.__timetableObject != None):
			self.__init__(self.__timetableObject['학교명'], self.__timetableObject['지역명'])

		self.__timetableObject = loads(self.__getResponseString(self.__URL + self.__basePath + self.__timetablePath, 'UTF-8'))

		return self

	def getPeriods(self: Comcigan) -> list[list[list[Union[list[Union[list[str, str], None]], None]]]]:
		if(self.__timetableObject == None):
			self.synchronize()

		try:
			subjects: list[str] = self.__timetableObject['긴자료' + self.__subjectId]
		except:
			raise Exception('Invalid self.__subjectId in module')

		try:
			teachers: list[str] = self.__timetableObject['자료' + self.__teacherId]
		except:
			raise Exception('Invalid self.__teacherId in module')

		for i in range(len(subjects)):
			if(subjects[i] != ''):
				if(subjects.index(subjects[i]) < i):
					if(subjects[i] == subjects[i + 1]):
						subjects[i] += 'A'
					else:
						subjects[i] += 'B'

				if(subjects[i + 1] == ''):
					break

		periods: list[list[list[Union[list[Union[list[str, str], None]], None]]]] = []
		
		try:
			periodIds = self.__timetableObject['자료' + self.__timetableId][1:]
		except:
			raise Exception('Invalid self.__timetableId in module')

		for i in range(len(periodIds)):
			periods.append([])

			gradeperiodIds = periodIds[i][1:]

			for j in range(len(gradeperiodIds)):
				periods[i].append([])

				classperiodIds = gradeperiodIds[j][1:]

				for k in range(len(classperiodIds)):
					periods[i][j].append([])

					periodIds = self.__getTrimmedArray(classperiodIds[k][1:])

					if(len(periodIds) != 0):
						for l in range(len(periodIds)):
							periods[i][j][k].append([])

							if(periodIds[l] != 0):
								subjectId = periodIds[l] % 100
								teacherId = int((periodIds[l] - subjectId) / 100)

								periods[i][j][k][l] = [subjects[subjectId], teachers[teacherId]]

							else:
								periods[i][j][k][l] = [None]
					else:
						periods[i][j][k].append(None)

		return periods

	def getSubjects(self: Comcigan) -> list[str]:
		if(self.__timetableObject == None):
			self.synchronize()

		try:
			return self.__getTrimmedArray(self.__timetableObject['긴자료' + self.__subjectId][1:])
		except:
			raise Exception('Invalid self.__subjectId in module')

	def getTeachers(self: Comcigan) -> list[str]:
		if(self.__timetableObject == None):
			self.synchronize()

		try:
			return self.__timetableObject['자료' + self.__teacherId][1:]
		except:
			raise Exception('Invalid self.__teacherId in module')

	def getPeriodStartingTimes(self: Comcigan) -> list[str]:
		if(self.__timetableObject == None):
			self.synchronize()

		periodTimes = self.__timetableObject['일과시간']

		for i in range(len(periodTimes)):
			periodTimes[i] = sub(r'\d+\(|\)', '', periodTimes[i])

		return periodTimes

	def getClassCounts(self: Comcigan) -> list[int]:
		if(self.__timetableObject == None):
			self.synchronize()

		return self.__timetableObject['학급수'][1:]

	def getHomeroomTeachers(self: Comcigan) -> list[list[str]]:
		if(self.__timetableObject == None):
			self.synchronize()

		teachers: list[str] = self.getTeachers()
		teachers.insert(0, '')

		homeroomTeachers: list[list[str]] = []

		for i in range(len(self.__timetableObject['담임'])):
			homeroomTeachers.append([])

			for teacherId in self.__getTrimmedArray(self.__timetableObject['담임'][i]):
				homeroomTeachers[i].append(teachers[teacherId])

		return homeroomTeachers
