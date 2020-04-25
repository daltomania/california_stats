import csv

input_data_directory = 'data'

# Check if the city's population is greater than 500,000
def city_meets_criteria(city_data):
	# be lazy and drop this row on the floor if it doesn't have every field
	if len(city_data) != 7:
		return False

	# get the city's population
	city_population = int(city_data[6])

	if (city_population > 500000):
		return True
	else:
		return False


# Read the city population file and filter for desired values
def read_and_filter_city_population_file(file_name):
	with open(input_data_directory + '/' + file_name) as csvfile:
		cityreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		half_million_person_cities = {}

		# read through each city
		for city in cityreader:
			if city_meets_criteria(city):
				city_name = city[0]
				city_population = int(city[6])
				half_million_person_cities[city_name] = {
					'population': city_population
				}

		return half_million_person_cities

# Read the offense file and add desired values to each city dictionary
def read_offenses_file_and_extract_values(file_name):
	with open(input_data_directory + '/' + file_name) as csvfile:
		cityreader = csv.reader(csvfile, delimiter=',', quotechar='"')

		# A dictionary of offenses by city
		offense_by_city = {}

		# read through each city and add it to a dictionary
		for city in cityreader:
			city_name = city[0]
			violent_crime = int(city[2].replace(',', ''))
			murder_and_non_negligent_manslaughter = int(city[3].replace(',', ''))

			offense_by_city[city_name] = {
				'violent_crime': violent_crime,
				'murder_and_non_negligent_manslaughter': murder_and_non_negligent_manslaughter
			}

		print(offense_by_city)
		return offense_by_city

# Combine our results across data sources
def combine_data_sources(half_million_person_cities, offense_by_city):
	combined_data = []

	for city in half_million_person_cities:
		city_name = city
		combined_data.append({
			'name': city_name,
			'population': half_million_person_cities[city_name]['population'],
			'violent_crime': offense_by_city[city_name]['violent_crime'],
			'murder_and_non_negligent_manslaughter': offense_by_city[city_name]['murder_and_non_negligent_manslaughter'],
		})

	return combined_data

# Output the results to a CSV
def output_results(file_name, final_city_data):
	with open(input_data_directory + '/' + file_name, 'w') as csvfile:
		field_names = ['name', 'population', 'violent_crime', 'murder_and_non_negligent_manslaughter']

		writer = csv.DictWriter(csvfile, fieldnames=field_names)

		for city in final_city_data:
			writer.writerow(city)

# Read and filter the city population file
half_million_person_cities = read_and_filter_city_population_file('california_city_populations.csv')

# Read the offense file and add desired values to each city dictionary
offense_by_city = read_offenses_file_and_extract_values('ca_offenses_by_city.csv')

# Combine our results across data sources
final_city_data = combine_data_sources(half_million_person_cities, offense_by_city)

# Write the result to an output file
output_results('output.csv', final_city_data)
