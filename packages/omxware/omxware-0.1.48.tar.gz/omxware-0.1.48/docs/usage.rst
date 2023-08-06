===============
Getting Started
===============


Import ``omxware`` and initialize session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import omxware

    token = omxware.get_token('omxware_username', 'omxware_pwd')
    omx = omxware.omxware(token)

Retrieve genes as a Pandas Dataframe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    search_string = 'sporulation'
    response = omx.genes(gene_name=search_string, page_size=25)
    
    #total_results = response.total_results()
    #print(total_results)
    
    results_df = response.results(type='df')
    results_df.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe table {
          border-collapse: collapse;
        }

        .dataframe th, td {
          padding: 8px;
          text-align: left;
          border-bottom: 1px solid #ddd;
        }

        .dataframe tr:hover {background-color:#f5f5f5;}
    </style>
    <table border="0.1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Genera</th>
          <th>Id</th>
          <th>Name</th>
          <th>Sequence_length</th>
          <th>Type</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>clostridioides</td>
          <td>e642254a70da3b1860b03d0755714862</td>
          <td>Sporulation kinase A</td>
          <td>1995</td>
          <td>gene</td>
        </tr>
        <tr>
          <th>1</th>
          <td>paenibacillus</td>
          <td>c22bd7d7ec6d836bfe7ca70caf9c0d56</td>
          <td>Sporulation kinase E</td>
          <td>1734</td>
          <td>gene</td>
        </tr>
        <tr>
          <th>2</th>
          <td>bacillus</td>
          <td>f5f7acff522419f65d867eef0d19376c</td>
          <td>Sporulation kinase E</td>
          <td>1788</td>
          <td>gene</td>
        </tr>
        <tr>
          <th>3</th>
          <td>bacillus</td>
          <td>48d934478603605b8d8540139585f460</td>
          <td>Sporulation protein YdcC</td>
          <td>1005</td>
          <td>gene</td>
        </tr>
        <tr>
          <th>4</th>
          <td>tindallia</td>
          <td>e9b4c151f00d03795645b289bb68e9a7</td>
          <td>Sporulation kinase A</td>
          <td>2109</td>
          <td>gene</td>
        </tr>
      </tbody>
    </table>
    </div>



Distribution of Genes by Genera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    response.show_facets(name='genera', topN=7)



.. image:: _static/output_5_0.png


Retrieve a Gene object as JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import json
    
    results_json = response.results(type='json')
    print(json.dumps(results_json[:3], indent=4, sort_keys=True))


.. parsed-literal::

    [
        {
            "genera": [
                "clostridioides"
            ],
            "id": "e642254a70da3b1860b03d0755714862",
            "name": "Sporulation kinase A",
            "sequence_length": 1995,
            "type": "gene"
        },
        {
            "genera": [
                "paenibacillus"
            ],
            "id": "c22bd7d7ec6d836bfe7ca70caf9c0d56",
            "name": "Sporulation kinase E",
            "sequence_length": 1734,
            "type": "gene"
        },
        {
            "genera": [
                "bacillus"
            ],
            "id": "f5f7acff522419f65d867eef0d19376c",
            "name": "Sporulation kinase E",
            "sequence_length": 1788,
            "type": "gene"
        }
    ]


Retrieve Gene data as an Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    results_list = response.results(type='list')
    
    # By default, the API returns a `list`
    print("Returns: List of {} objects \nResults: {}\n".format(response.type(), response.total_results()) )
        
    gene = results_list[0]
    print("Id  \t\t=> " + gene.id())
    print("Name   \t\t=> " + gene.name())
    print("Sequence   \t=> " + gene.sequence()[:100] + "...")
    print("Sequence length => " + str(gene.sequence_length()))
    
    print("\n\n JSON:")
    print(gene.json())


.. parsed-literal::

    Returns: List of gene objects 
    Results: 73318
    
    Id  		=> e642254a70da3b1860b03d0755714862
    Name   		=> Sporulation kinase A
    Sequence   	=> GTGAATAAAAAAAAGATTGTTATTATAGGGATTATTTATTCATTTTTAGTAGTATTTTCACTTACAAATATGTATGTAAATATGGAGTATAATCTAAATG...
    Sequence length => 1995
    
    
     JSON:
    {'id': 'e642254a70da3b1860b03d0755714862', 'name': 'Sporulation kinase A', 'type': 'gene', 'genera': ['clostridioides'], 'sequence_length': 1995}


Retrieve a Gene in FASTA format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    new_gene_object = omx.genes(ids='00054a98f8ddd95e3f46d9d757137284').results(type='fasta')
    print(new_gene_object)


.. parsed-literal::

    >OMX_gene_00054a98f8ddd95e3f46d9d757137284|Sporulation initiation phosphotransferase F
    ATGAACGAGAAGGTGCTGCTGGTTGACGACGACGAGGCCATCCGCGAAGTCCTCAGCCTCTCCATCGCCGACCTGGGCTACGACGTGGAAACCGCCCCCGGCGGCCGCGAAGCCCTGGAGCTGTGCGCCACCTTCAAACCGTCCATCGTGCTCACCGACATCAAGATGCCCGGCATGGACGGCATCGAACTGCTCTCGCGCGTCAAAGCCCTCGATCCCGAGATCGAGGTCATCATGATTTCCGGCCATGGCGACATGGAACTGGCCATCGAGAGCCTCAAGCGCCAGGCCCTGGATTTCCTCACCAAGCCCGTGCGCGACGAACTGCTCACAGCCTCCCTCCACCGGGCCGCCGACCGCGTGTCCATGCGCCGCCAGATCACCGAACACACCCGCAATCTCGAACGGCTGGTGCGCGAAAAATCCGCCCGCCTGGTCGAGATGGAGCGCCGCATGGCCGTGGGGCAGGCCGTGGAGGGCGTGGCCAGCGCCATCGAGGGGCTCATTGCCTCCTTCGACCAGGGACCCAGCTATTTCAACCAGATGCCCTGCTGCATCGTCATCCACAACCGCTACCTCGAAATCGTGGCCGTAAACACCCTGGGCCGGCAGCGCCTGGGCGAGGTGGTGGGCAAGATGAGCTGGGAACTCTACGCCGACCGTCAGGGCAGCGGCAACGCCTGCCCGGTCTGGCGCACCGTGGAACAAGGCCAGGGCCAGCGCGGCCGCGAGACCTTCCGCGACAAGGACGGCCGCGAGATTCCGGTGCTGATCCATACCGCCCCGGTCTTCGGCACGGACGGCCAGGTGGAGCTGGTCATCGAGATCGCCGCCGACGTGGCCGAGGTGGGCCGGCTCCAGGAAGAGCTGCGGGCCGTGCGCGAGAAATTCCAGCGCCTGTTCGACGCCGTGCCCTGCGCCATCGCCGTGCTGGACCAGGACTTCACCGTGGTCGAAGCCAACCGCCAATGGCGCGCCGACTTCGGCGAGGCCGAAACCGGCCCCTGCCACAAACTGTTTGCCCACCGCGACGACCCCTGCGAACACTGCCCGGCCGAAAGCTCCTTCCACGACGGCGCGCCCCACGAAGGCGAAACTGTCGTGTCCACCCGCTGCGGCGCGGCCAAAAACATGTGGCTTCGCACCGCCCCCATCCCCGACGCCACAGGCGAAACCAGCCAGGTCATCGAAATCGCCGCCGACATCACCCCCATCCGGGCCCTGCAAGACCACCTCGCATCGCTTGGGCTCATGCTCGGCTCCATGTCCCACGGCGTCAAAGGCCTGCTCACCTCCCTCGACGGCGGCATGTTCAAGGTCGAAACCGGACTGTCCCGCGAGGACTGGACCCGCGTGCGCGACGGTTGGGGCGTGGTGTCCGACAAGATCGGACGCATCCGCAACATGGTGCTCGACATCCTGTGGTACGCCAAATCGCGCGAACCCGAGCTCTCCCCCGTCTCCATCGAAACCTTCGCCCGCGATCTGGCCGGCATCGTCGAACCCAAGGCCCAAAGCCGCGACGTGGCCTTCATCCTGCGCCTGGGCGAGGCCGCAGGCACGCTGCCCATGGACGAGACGGCGCTCACCTCGGCCATGGTCAACCTGCTCGAAAACGCCGTGGATGCCTGCGCCGAGGACAAGGCCAAGGCCTTCCACGAAGTGACCCTGACCGTGGAAGCCACGGCCGAGGCCGTGACCTTCGTGGTCGCCGACAACGGCGTCGGCATGGACCAGTCCACCCGGGAACGCATGTTTACGCTCTTTTTCTCCTCCAAAGGCTCGCGCGGCACCGGACTGGGGCTTTTCATCGCCAACCAGATCGTGGCCCAGCACGGAGGCTCCATCGCCGTGACCTCCGAACCCGGCGTCGGCAGCGCCATCGCCGTGCGCCTGCCGCGCGGCGCTAGCGTTTGCAGTTAG
