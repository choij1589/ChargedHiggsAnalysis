hist_configs = {
    # muons
    "Inputs/muons/1/pt": {"x_title": "p_{T}(#mu1) [GeV]",
                   "y_title": "Events / 5 GeV",
                   "x_range": [0., 250.],
                   "rebin": 5},
    "Inputs/muons/1/eta": {"x_title": "#eta(#mu1)",
                    "y_title": "Events",
                    "x_range": [-2.4, 2.4],
                    "rebin": 5},
    "Inputs/muons/1/phi": {"x_title": "#phi(#mu1)",
                    "y_title": "Events",
                    "x_range": [-3.2, 3.2],
                    "rebin": 4},
    "Inputs/muons/2/pt": {"x_title": "p_{T}(#mu2) [GeV]",
                   "y_title": "Events / 5 GeV",
                   "x_range": [0., 200.],
                   "rebin": 5},
    "Inputs/muons/2/eta": {"x_title": "#eta(#mu2)",
                    "y_title": "Events",
                    "x_range": [-2.4, 2.4],
                    "rebin": 5},
    "Inputs/muons/2/phi": {"x_title": "#phi(#mu2)",
                    "y_title": "Events",
                    "x_range": [-3.2, 3.2],
                    "rebin": 4},
    "Inputs/muons/3/pt": {"x_title": "p_{T}(#mu3) [GeV]",
                   "y_title": "Events / 5 GeV",
                   "x_range": [0., 150.],
                   "rebin": 5},
    "Inputs/muons/3/eta": {"x_title": "#eta(#mu3)",
                    "y_title": "Events",
                    "x_range": [-2.4, 2.4],
                    "rebin": 5},
    "Inputs/muons/3/phi": {"x_title": "#phi(#mu3)",
                    "y_title": "Events",
                    "x_range": [-3.2, 3.2],
                    "rebin": 4}, 
    # jets
    "Inputs/jets/1/pt": {"x_title": "p_{T}(j1) [GeV]",
                  "y_title": "Events / 10 GeV",
                  "x_range": [0., 300.],
                  "rebin": 10
                  },
    "Inputs/jets/1/eta": {"x_title": "#eta(j1)",
                   "y_title": "Events",
                   "x_range": [-2.4, 2.4],
                   "rebin": 5
                   },
    "Inputs/jets/1/phi": {"x_title": "#phi(j1)",
                   "y_title": "Events",
                   "x_range": [-3.2, 3.2],
                   "rebin": 4
                   },
    "Inputs/jets/1/mass": {"x_title": "M(j1)",
                    "y_title": "Events / GeV",
                    "x_range": [0., 20.],
                    },
    "Inputs/jets/2/pt": {"x_title": "p_{T}(j2) [GeV]",
                  "y_title": "Events / 10 GeV",
                  "x_range": [0., 250.],
                  "rebin": 10
                  },
    "Inputs/jets/2/eta": {"x_title": "#eta(j2)",
                   "y_title": "Events",
                   "x_range": [-2.4, 2.4],
                   "rebin": 5
                   },
    "Inputs/jets/2/phi": {"x_title": "#phi(j2)",
                   "y_title": "Events",
                   "x_range": [-3.2, 3.2],
                   "rebin": 4
                   },
    "Inputs/jets/2/mass": {"x_title": "M(j2)",
                    "y_title": "Events / GeV",
                    "x_range": [0., 20.],
                    },
    "Inputs/jets/3/pt": {"x_title": "p_{T}(j3) [GeV]",
                  "y_title": "Events / 10 GeV",
                  "x_range": [0., 200.],
                  "rebin": 10
                  },
    "Inputs/jets/3/eta": {"x_title": "#eta(j3)",
                   "y_title": "Events",
                   "x_range": [-2.4, 2.4],
                   "rebin": 5
                   },
    "Inputs/jets/3/phi": {"x_title": "#phi(j3)",
                   "y_title": "Events",
                   "x_range": [-3.2, 3.2],
                   "rebin": 4
                   },
    "Inputs/jets/3/mass": {"x_title": "M(j3)",
                    "y_title": "Events / GeV",
                    "x_range": [0., 20.],
                    },
    "Inputs/jets/4/pt": {"x_title": "p_{T}(j4) [GeV]",
                  "y_title": "Events / 10 GeV",
                  "x_range": [0., 200.],
                  "rebin": 10
                  },
    "Inputs/jets/4/eta": {"x_title": "#eta(j4)",
                   "y_title": "Events",
                   "x_range": [-2.4, 2.4],
                   "rebin": 5
                   },
    "Inputs/jets/4/phi": {"x_title": "#phi(j4)",
                   "y_title": "Events",
                   "x_range": [-3.2, 3.2],
                   "rebin": 4
                   },
    "Inputs/jets/4/mass": {"x_title": "M(j4)",
                    "y_title": "Events / GeV",
                    "x_range": [0., 20.],
                    },
    "Inputs/jets/size": {"x_title": "N_{j}",
                  "y_title": "Events",
                  "x_range": [0., 10.]
                  },
    "Inputs/jets/HT": {"x_title": "H_{T} [GeV]",
                "y_title": "Events / 10 GeV",
                "x_range": [0., 1000.],
                "rebin": 10
                },
    # ZCand
    "Inputs/ZCand/pt": {"x_title": "p_{T}(Z) [GeV]",
                 "y_title": "Events / 5 GeV",
                 "x_range": [0., 200.],
                 "rebin": 5
                 },
    "Inputs/ZCand/eta": {"x_title": "#eta(Z)",
                  "y_title": "Events",
                  "x_range": [-5., 5.],
                  "rebin": 10
                  },
    "Inputs/ZCand/phi": {"x_title": "#phi(Z)",
                  "y_title": "Events",
                  "x_range": [-3.2, 3.2],
                  "rebin": 8
                  },
    "Inputs/ZCand/mass": {"x_title": "M(Z) [GeV]",
                   "y_title": "Events / 2 GeV",
                   "x_range": [75., 105.],
                   "rebin": 2
                   },
    "Inputs/xZCand/pt": {"x_title": "p_{T}(xZ) [GeV]",
                 "y_title": "Events / 5 GeV",
                 "x_range": [0., 200.],
                 "rebin": 5
                 },
    "Inputs/xZCand/eta": {"x_title": "#eta(xZ)",
                  "y_title": "Events",
                  "x_range": [-5., 5.],
                  "rebin": 5
                  },
    "Inputs/xZCand/phi": {"x_title": "#phi(xZ)",
                  "y_title": "Events",
                  "x_range": [-3.2, 3.2],
                  "rebin": 8
                  },
    "Inputs/xZCand/mass": {"x_title": "M(xZ) [GeV]",
                   "y_title": "Events / 5 GeV",
                   "x_range": [0., 300.],
                   "rebin": 5
                   },
    # Outputs
    "Outputs/MHc-70_MA-15/ACand/pt": {"x_title": "p_{T}(A)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-70_MA-15/ACand/eta": {"x_title": "#eta(A)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 5
                                       },
    "Outputs/MHc-70_MA-15/ACand/phi": {"x_title": "#phi(A)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-70_MA-15/ACand/mass": {"x_title": "m(A)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-70_MA-15/xACand/pt": {"x_title": "p_{T}(xA)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-70_MA-15/xACand/eta": {"x_title": "#eta(xA)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 10
                                       },
    "Outputs/MHc-70_MA-15/xACand/phi": {"x_title": "#phi(xA)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-70_MA-15/xACand/mass": {"x_title": "m(xA)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-70_MA-15/score_vs_TTLL_powheg": {"x_title": "score",
                                                 "y_title": "Events",
                                                 "x_range": [0., 1.],
                                                 "rebin": 5
                                                 },
    "Outputs/MHc-70_MA-15/score_vs_ttX": {"x_title": "score",
                                          "y_title": "Events",
                                          "x_range": [0., 1.],
                                          "rebin": 5
                                         },
    "Outputs/MHc-100_MA-60/ACand/pt": {"x_title": "p_{T}(A)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-100_MA-60/ACand/eta": {"x_title": "#eta(A)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 5
                                       },
    "Outputs/MHc-100_MA-60/ACand/phi": {"x_title": "#phi(A)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-100_MA-60/ACand/mass": {"x_title": "m(A)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-100_MA-60/xACand/pt": {"x_title": "p_{T}(xA)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-100_MA-60/xACand/eta": {"x_title": "#eta(xA)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 10
                                       },
    "Outputs/MHc-100_MA-60/xACand/phi": {"x_title": "#phi(xA)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-100_MA-60/xACand/mass": {"x_title": "m(xA)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-100_MA-60/score_vs_TTLL_powheg": {"x_title": "score",
                                                 "y_title": "Events",
                                                 "x_range": [0., 1.],
                                                 "rebin": 5
                                                 },
    "Outputs/MHc-100_MA-60/score_vs_ttX": {"x_title": "score",
                                          "y_title": "Events",
                                          "x_range": [0., 1.],
                                          "rebin": 5
                                         },
    "Outputs/MHc-130_MA-90/ACand/pt": {"x_title": "p_{T}(A)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-130_MA-90/ACand/eta": {"x_title": "#eta(A)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 5
                                       },
    "Outputs/MHc-130_MA-90/ACand/phi": {"x_title": "#phi(A)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-130_MA-90/ACand/mass": {"x_title": "m(A)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-130_MA-90/xACand/pt": {"x_title": "p_{T}(xA)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-130_MA-90/xACand/eta": {"x_title": "#eta(xA)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 10
                                       },
    "Outputs/MHc-130_MA-90/xACand/phi": {"x_title": "#phi(xA)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-130_MA-90/xACand/mass": {"x_title": "m(xA)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-130_MA-90/score_vs_TTLL_powheg": {"x_title": "score",
                                                 "y_title": "Events",
                                                 "x_range": [0., 1.],
                                                 "rebin": 5
                                                 },
    "Outputs/MHc-130_MA-90/score_vs_ttX": {"x_title": "score",
                                          "y_title": "Events",
                                          "x_range": [0., 1.],
                                          "rebin": 5
                                         },
    "Outputs/MHc-160_MA-155/ACand/pt": {"x_title": "p_{T}(A)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-160_MA-155/ACand/eta": {"x_title": "#eta(A)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 5
                                       },
    "Outputs/MHc-160_MA-155/ACand/phi": {"x_title": "#phi(A)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-160_MA-155/ACand/mass": {"x_title": "m(A)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-160_MA-155/xACand/pt": {"x_title": "p_{T}(xA)",
                                      "y_title": "Events / 5 GeV",
                                      "x_range": [0., 200.],
                                      "rebin": 5
                                      },
    "Outputs/MHc-160_MA-155/xACand/eta": {"x_title": "#eta(xA)",
                                       "y_title": "Events",
                                       "x_range": [-5., 5.],
                                       "rebin": 5
                                       },
    "Outputs/MHc-160_MA-155/xACand/phi": {"x_title": "#phi(xA)",
                                       "y_title": "Events",
                                       "x_range": [-3.2, 3.2],
                                       "rebin": 8
                                       },
    "Outputs/MHc-160_MA-155/xACand/mass": {"x_title": "m(xA)",
                                        "y_title": "Events / 5 GeV",
                                        "x_range": [0., 200.],
                                        "rebin": 5
                                        },
    "Outputs/MHc-160_MA-155/score_vs_TTLL_powheg": {"x_title": "score",
                                                 "y_title": "Events",
                                                 "x_range": [0., 1.],
                                                 "rebin": 5
                                                 },
    "Outputs/MHc-160_MA-155/score_vs_ttX": {"x_title": "score",
                                          "y_title": "Events",
                                          "x_range": [0., 1.],
                                          "rebin": 5
                                         },
}